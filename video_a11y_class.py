# Define a video a11y class
# Get general information of a YouTube video
# Calculates accessibility heuristics of a YouTube video
# Input: a YouTube video id
# Output: a json file of a11y heuristics scores/counts

import sys
import youtube_dl

# A video class
class Video:
    def __init__(self, video_id):
        self.video_id = video_id

    #def myfunc(self):

### GET VIDEO INFORMATION ###


### DOWNLOAD VIDEO, AUDIO, CAPTIONS ###
