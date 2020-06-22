import numpy as np 
import pandas as pd 
import isodate
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from youtube_transcript_api._errors import NoTranscriptAvailable
from youtube_transcript_api._errors import NoTranscriptFound
from youtube_transcript_api._errors import VideoUnavailable


df = pd.read_csv("new_samples_trending.csv")

for i in range(len(df["id"])):
    print(str(i) + "/" + str(len(df["id"])))
    video_id = df["id"][i]
    video_dur = df["duration"][i]

    try:
        cc = YouTubeTranscriptApi.get_transcript(video_id)
        #print(cc)
    except (TranscriptsDisabled, NoTranscriptAvailable, 
        NoTranscriptFound, VideoUnavailable) as err:
        print("No CC for this video!")
        continue

    df_new = pd.DataFrame(cc)
    df_new["id"] = video_id
    df_new["videoDuration"] = video_dur
    df_new["end"] = round(df_new["start"] + df_new["duration"], 3)
    df_new["proportion"] = round(sum(df_new["duration"])/df_new["videoDuration"], 3)

    df_new = df_new[['id', 'text', 'start', 'end', 'duration', 'videoDuration', 'proportion']]

    filename = "cc/" + str(video_id) + ".csv"
    df_new.to_csv(filename, index=False)
   

    