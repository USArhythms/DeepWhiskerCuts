from MovieTools import make_movie_and_stimulus_file,save_trial_n,extract_eye_videos
import re
import deeplabcut
import os
import shutil
from top_view_spliter import split_left_and_right_from_top_video
from setting import this_computer

def processs_side_view_data(data_path):
    make_movie_and_stimulus_file(data_path,parallel=False,ncores = 4)
    save_trial_n(data_path)
    videos  = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.analyze_videos(this_computer['side_view_config'],videos,shuffle=2, save_as_csv=True )
    deeplabcut.filterpredictions(this_computer['side_view_config'],videos,shuffle=2, save_as_csv=True )
    extract_eye_videos(data_path,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle1_271000')
    extract_eye_videos(data_path,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle2_500000_filtered')
    eye_videos = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('EYE.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.analyze_videos(this_computer['eye_config'],eye_videos,shuffle=3, save_as_csv=True )
    deeplabcut.filterpredictions(this_computer['eye_config'],eye_videos,shuffle=3)
    # shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)

def processs_top_view_data(data_path):
    make_movie_and_stimulus_file(data_path,parallel=True,ncores = 16)
    save_trial_n(data_path)
    text_files = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('video.mp4') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.analyze_videos(this_computer['head_config'],text_files,shuffle=1, save_as_csv=True )
    deeplabcut.filterpredictions(this_computer['head_config'],text_files)
    split_left_and_right_from_top_video(data_path)
    XfilesL = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mask')  ] # find all files with R.avi as file name
    XfilesR = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mirror')  ] # find all files with R.avi as file name
    deeplabcut.analyze_videos(this_computer['top_view_config'],XfilesL,shuffle=1, save_as_csv=True)
    deeplabcut.filterpredictions(this_computer['top_view_config'],XfilesL,shuffle=1)
    deeplabcut.analyze_videos(this_computer['top_view_config'],XfilesR,shuffle=1, save_as_csv=True)
    deeplabcut.filterpredictions(this_computer['top_view_config'],XfilesR,shuffle=1)
    # shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)
