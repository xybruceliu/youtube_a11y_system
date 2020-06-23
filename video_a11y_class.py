# Define a video a11y class
# Get general information of a YouTube video
# Calculates accessibility heuristics of a YouTube video
# Input: a YouTube video id
# Output: a json file of a11y heuristics scores/counts

import sys
import os
import os.path
import pandas as pd
import numpy as np
import youtube_dl
from get_info import get_video_info
from get_cc import get_cc
from compute_a11y.compute_text_a11y import entropy1, word_count, lexical_density
from compute_a11y.compute_visual_a11y import dl_video, find_scenes
from compute_a11y.compute_non_dialog import download_captions, process_captions, compute_non_dialog_percentage

# A video class
class Video:
    def __init__(self, video_id):

        # Create directories if not exist
        dirs = ['audio', 'caption', 'gaps', 'scenes', 'tmp', 'video', 'words']
        for dir_name in dirs:
            if not os.path.exists(dir_name): os.makedirs(dir_name)

        self.id = video_id

        # Get video information     
        self.info = get_video_info(self.id)
        self.duration = self.info['duration']
        self.category = self.info['category']

        # Get captions
        self.captions = get_cc(self.id)


    ###########################
    ### TEXT INFORMATION ###

    # word count of captions
    def captions_word_count(self):
        return word_count(self.captions)

    # compute text entropy of captions
    # ref: https://www.aclweb.org/anthology/P19-1101.pdf
    def captions_entropy(self):
        return entropy1(self.captions)
    
    # compute lexical density of captions 
    # ref: https://en.wikipedia.org/wiki/Lexical_density
    def captions_lexical_density(self):
        return lexical_density(self.captions)


    ###########################
    ### VISUAL INFORMATION ###

    # download the video to a local dir
    def download_video(self):
        dl_video(self.id, "video/")

    # find scenes in the video and save scene information to two .csv files
    # ref: https://pyscenedetect.readthedocs.io/en/latest/
    def detect_scenes(self):
        file_path = "video/" + str(self.id) + ".mp4"

        if not os.path.exists(file_path):
            self.download_video()
        
        return find_scenes(self.id, "video/", "scenes/")
    

    # count number of scenes of the video
    def num_scenes(self):
        file_path = "scenes/" + str(self.id) + ".csv"

        if not os.path.exists(file_path):
            self.detect_scenes()
        
        df = pd.read_csv(file_path)
        return len(df)

    # compute the average hsv change per frame of the video
    def avg_hsv_change(self):
        file_path = "scenes/" + str(self.id) + "_stats.csv"

        if not os.path.exists(file_path):
            self.detect_scenes()
        
        df = pd.read_csv(file_path, skiprows=1)
        return np.mean(df['content_val'])

    # compute the percentage of non-diaglogue in the video
    def non_dialog_percentage(self):
        file_path = "caption/" + str(self.id) + ".vtt.en.vtt"

        if not os.path.exists(file_path):
            download_captions(self.id, "caption/")

        caption_path = "caption/" + str(self.id) + ".vtt.en.vtt"
        words_path = "words/" + str(self.id) + "_words.json"
        gaps_path = "gaps/" + str(self.id) + "_gaps.json"
        process_captions(self.id, caption_path, words_path, "tmp/")

        percentage = compute_non_dialog_percentage(self.id, self.duration, words_path, gaps_path)

        return percentage
            