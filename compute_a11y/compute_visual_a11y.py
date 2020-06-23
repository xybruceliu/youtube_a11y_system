import os
import scenedetect
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector
import youtube_dl
import pandas as pd

def dl_video(video_id, path):
    video_link = "https://www.youtube.com/watch?v=" + str(video_id)
    ydl_opts = {'format': 'mp4',
                'outtmpl': path+str(video_id)+'.%(ext)s',}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

def find_scenes(video_id, video_path, scenes_path):
    # type: (str) -> List[Tuple[FrameTimecode, FrameTimecode]]
    video_manager = VideoManager([video_path+video_id+".mp4"])
    stats_manager = StatsManager()
    # Construct our SceneManager and pass it our StatsManager.
    scene_manager = SceneManager(stats_manager)

    # Add ContentDetector algorithm (each detector's constructor
    # takes detector options, e.g. threshold).
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    # We save our stats file to {VIDEO_PATH}.stats.csv.
    stats_file_path = scenes_path+video_id+"_stats.csv"
    scenes_file_path = scenes_path+video_id+".csv"

    scene_list = []

    try:
        # If stats file exists, load it.
        if os.path.exists(stats_file_path):
            # Read stats from CSV file opened in read mode:
            with open(stats_file_path, 'r') as stats_file:
                stats_manager.load_from_csv(stats_file, base_timecode)

        # Set downscale factor to improve processing speed.
        video_manager.set_downscale_factor()

        # Start video_manager.
        video_manager.start()

        # Perform scene detection on video_manager.
        scene_manager.detect_scenes(frame_source=video_manager)

        # Obtain list of detected scenes.
        scene_list = scene_manager.get_scene_list(base_timecode)
        # Each scene is a tuple of (start, end) FrameTimecodes.

        df = pd.DataFrame(columns=['scene', 'start', 'start_frame', 'end', 'end_frame'])

        #print('List of scenes obtained:')
        for i, scene in enumerate(scene_list):
            # print(
            #     'Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
            #     i+1,
            #     scene[0].get_timecode(), scene[0].get_frames(),
            #     scene[1].get_timecode(), scene[1].get_frames(),))

            df = df.append({'scene': i+1, 
                            'start': scene[0].get_timecode(), 
                            'start_frame': scene[0].get_frames(), 
                            'end': scene[1].get_timecode(), 
                            'end_frame': scene[1].get_frames()}, 
                            ignore_index=True)

        # We only write to the stats file if a save is required:
        if stats_manager.is_save_required():
            with open(stats_file_path, 'w') as stats_file:
                stats_manager.save_to_csv(stats_file, base_timecode)

        df.to_csv(scenes_file_path, index=False)

    finally:
        video_manager.release()

    return

