from DeepWhiskerCuts.lib.MovieTools import make_movie_for_all_trials,extract_eye_videos
import deeplabcut
import os
from DeepWhiskerCuts.lib.top_view_spliter import split_left_and_right_from_top_video
from DeepWhiskerCuts.setting.setting import this_computer
from DeepWhiskerCuts.setting.dlc_setting import side_view_shuffle,eye_shuffle,whisker_shuffle,top_shuffle
from tqdm import tqdm
import pdb

def processs_side_view_data(data_path):
    # make_movie_for_all_trials(data_path,parallel=False,ncores=4)
    analyze_side_view_video(data_path)
    extract_eye_videos(data_path,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle1_271000')
    analyze_eye_video(data_path)

def processs_top_view_data(data_path):
    make_movie_for_all_trials(data_path,parallel=False,ncores=4)
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

def analyze_side_view_video(data_path,shuffle=side_view_shuffle):
    videos  = get_side_videos(data_path)
    analyze_videos(videos,'side_view_config',shuffle=shuffle)

def get_eye_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('EYE.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]

def get_top_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('video.mp4') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]

def analyze_eye_video(data_path,shuffle=eye_shuffle):
    eye_videos = get_eye_videos(data_path)
    analyze_videos(eye_videos,'eye_config',shuffle=shuffle)

def analyze_top_view_video(data_path,shuffle=top_shuffle):
    try:
        top_videos = get_top_videos(data_path)
        analyze_videos(top_videos,'top_view_config',shuffle=shuffle)
    except:
        pdb.set_trace()

def get_left_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mask')  ]

def analyze_left_video(data_path,shuffle=left_shuffle):
    left_videos = get_left_videos(data_path)
    analyze_videos(left_videos,'whisker_config',shuffle=shuffle)

def get_right_videos(data_path):
    return [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mirror')  ] 

def analyze_right_video(data_path,shuffle=right_shuffle):
    right_videos = get_right_videos(data_path)
    analyze_videos(right_videos,'whisker_config',shuffle=shuffle)

def run_dlc_with_error_handling(videos,deeplabcut_function):
    for videoi in tqdm(range(len(videos)),'processing videos'): 
        video = videos[videoi]
        try:
            deeplabcut_function(video)
        except BaseException as ex:
            pdb.set_trace()