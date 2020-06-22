import sys
from video_a11y_class import Video


video_id = sys.argv[1]
test_video = Video(video_id)
 
print(test_video.captions_lexical_density())