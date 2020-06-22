# Define a video a11y class
# Get general information of a YouTube video
# Calculates accessibility heuristics of a YouTube video
# Input: a YouTube video id
# Output: a json file of a11y heuristics scores/counts

import sys
import youtube_dl
from get_video_info import get_video_info
from get_cc import get_cc
from compute_a11y.compute_text_a11y import entropy1, word_count, lexical_density

# A video class
class Video:
    def __init__(self, video_id):
        self.id = video_id

        # Get video information     
        self.info = get_video_info(self.id)
        self.duration = self.info['duration']
        self.category = self.info['category']

        # Get captions
        self.captions = get_cc(self.id)
    

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


    ### DOWNLOAD VIDEO, AUDIO, CAPTIONS ###
