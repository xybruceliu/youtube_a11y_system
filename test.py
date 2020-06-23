import sys
from video_a11y_class import Video

#video_id = sys.argv[1]
video_id = "Ty92wz0K-CM"
test_video = Video(video_id)

print("word count: ", test_video.captions_word_count())
print("text entropy of captions: ", test_video.captions_entropy())
print("lexical density of captions: ", test_video.captions_lexical_density())
print("number of scenes in the video: ", test_video.num_scenes())
print("hsv change per frame: ", test_video.avg_hsv_change())
print("non dialogue percentage: ", test_video.non_dialog_percentage())