from MovieTools import make_movie_and_stimulus_file,extract_eye_videos
import deeplabcut
import os
from top_view_spliter import split_left_and_right_from_top_video
from setting import this_computer
import pdb
from tqdm import tqdm
def processs_side_view_data(data_path):
    make_movie_and_stimulus_file(data_path,parallel=False,ncores = 4)
    analyze_side_view_video(data_path)
    extract_eye_videos(data_path,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle1_271000')
    analyze_eye_video(data_path)

def processs_top_view_data(data_path):
    make_movie_and_stimulus_file(data_path,parallel=True,ncores = 16)
    analyze_top_view_video(data_path)
    split_left_and_right_from_top_video(data_path)
    analyze_left_video(data_path)
    analyze_right_video(data_path)

def analyze_video(config,video,shuffle):
    deeplabcut.analyze_videos(config,[video],shuffle=shuffle, save_as_csv=True )
    deeplabcut.filterpredictions(config,[video],shuffle=shuffle, save_as_csv=True )

def analyze_videos(videos,config_type,shuffle=2):
    def deeplabcut_function(video):
        analyze_video(this_computer[config_type],video,shuffle=shuffle)
    run_dlc_with_error_handling(videos,deeplabcut_function)

def get_side_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]

def analyze_side_view_video(data_path,shuffle=2):
    videos  = get_side_videos(data_path)
    analyze_videos(videos,'side_view_config',shuffle=shuffle)

def get_eye_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('EYE.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]

def get_top_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('video.mp4') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]

def analyze_eye_video(data_path,shuffle=3):
    eye_videos = get_eye_videos(data_path)
    analyze_videos(eye_videos,'eye_config',shuffle=shuffle)

def analyze_top_view_video(data_path,shuffle=1):
    top_videos = get_top_videos(data_path)
    analyze_videos(top_videos,'head_config',shuffle=shuffle)

def get_left_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mask')  ]

def analyze_left_video(data_path,shuffle=1):
    left_videos = get_left_videos(data_path)
    analyze_videos(left_videos,'top_view_config',shuffle=shuffle)

def get_right_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mirror')  ] 

def analyze_right_video(data_path,shuffle=1):
    right_videos = get_right_videos(data_path)
    analyze_videos(right_videos,'top_view_config',shuffle=shuffle)

def run_dlc_with_error_handling(videos,deeplabcut_function):
    for videoi in tqdm(range(len(videos)),'processing videos'): 
        video = videos[videoi]
        try:
            deeplabcut_function(video)
        except BaseException as ex:
            ...