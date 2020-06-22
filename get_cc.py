import numpy as np 
import pandas as pd 
import isodate
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from youtube_transcript_api._errors import NoTranscriptAvailable
from youtube_transcript_api._errors import NoTranscriptFound
from youtube_transcript_api._errors import VideoUnavailable

def get_cc(video_id):

    try:
        cc = YouTubeTranscriptApi.get_transcript(video_id)
        
    except (TranscriptsDisabled, NoTranscriptAvailable, 
        NoTranscriptFound, VideoUnavailable) as err:
        print("No CC for this video!")
        return None

    df_new = pd.DataFrame(cc)
    filename = "caption_examples/" + str(video_id) + "_timestamp" + ".csv"
    df_new.to_csv(filename, index=False)

    captions = ''.join(df_new['text'])
    txtname = "caption_examples/" + str(video_id) + ".txt"
    with open(txtname, "w") as text_file:
        text_file.write(captions)

    return captions
   

    