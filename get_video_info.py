from pyyoutube import Api
import pandas as pd 
import numpy as np
from pyyoutube.models import VideoTopicDetails
import isodate

api = Api(api_key='AIzaSyDWmzW7AjG7H3ScJLzXuM63_EjG9zd8WW8')

category_dict = {
1:"Film & Animation", 
2:"Autos & Vehicles", 
10:"Music",
15:"Pets & Animals",
17: 'Sports',
18: 'Short Movies',
19: 'Travel & Events',
20: 'Gaming',
21: 'Videoblogging',
22: 'People & Blogs',
23: 'Comedy',
24: 'Entertainment',
25: 'News & Politics',
26: 'Howto & Style',
27: 'Education',
28: 'Science & Technology',
29: 'Nonprofits & Activism',
30: 'Movies',
31: 'Anime/Animation',
32: 'Action/Adventure',
33: 'Classics',
34: 'Comedy',
35: 'Documentary',
36: 'Drama',
37: 'Family',
38: 'Foreign',
39: 'Horror',
40:'Sci-Fi/Fantasy',
41: 'Thriller',
42: 'Shorts',
43: 'Shows',
44: 'Trailers'}

def 


for i in range(1000, 1350):
    id_str = str(df["ID"][i])
    print(str(i)+"/"+str(len(df["ID"])))
    print(id_str)
    # video information

    video_by_id = api.get_video_by_id(video_id=id_str)
    if (len(video_by_id.items) == 0): 
        print('Invalid video id!')
        continue
    video = video_by_id.items[0]

    snippet = video.snippet
    statistics = video.statistics
    contentDetails = video.contentDetails
    topicDetails = video.topicDetails

    try:
        topicCategories = topicDetails.topicCategories
    except AttributeError as err:
        print("No topic categories!")
        topicCategories = []

    # channel information
    channel_by_id = api.get_channel_info(channel_id=snippet.channelId)
    channel = channel_by_id.items[0]

    # creating dataframe, add in data
    df_new = df_new.append({'id': id_str, 
        'title': snippet.title,
        'channelId': snippet.channelId,
        'channelTitle': snippet.channelTitle,
        'channelDescription': channel.snippet.description,
        'channelLiked': channel.contentDetails.relatedPlaylists.likes,
        'channelSubs': channel.statistics.subscriberCount, 
        'description': snippet.description,
        'duration': isodate.parse_duration(contentDetails.duration).total_seconds(),
        'caption': contentDetails.caption,
        'views':statistics.viewCount, 
        'likes': statistics.likeCount,
        'dislikes':statistics.dislikeCount,
        'comments': statistics.commentCount,
        'tags':snippet.tags, 
        'categoryId': snippet.categoryId,
        'category':category_dict[int(snippet.categoryId)], 
        'topicCategories':[sub.replace('https://en.wikipedia.org/wiki/', '') for sub in topicCategories]}, ignore_index=True)



df_new.to_csv("new_samples_trending.csv", index=False)