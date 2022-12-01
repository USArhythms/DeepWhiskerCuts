from MovieTools import make_movie_and_stimulus_file,extract_eye_videos
import deeplabcut
import os
from top_view_spliter import split_left_and_right_from_top_video
from setting import this_computer

def processs_side_view_data(data_path):
    make_movie_and_stimulus_file(data_path,parallel=False,ncores = 4)
    analyze_side_view_video(data_path)
    extract_eye_videos(data_path,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle1_271000')
    analyze_eye_video(data_path)
    # shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)

def processs_top_view_data(data_path):
    make_movie_and_stimulus_file(data_path,parallel=True,ncores = 16)
    analyze_top_view_video(data_path)
    split_left_and_right_from_top_video(data_path)
    analyze_left_video(data_path)
    analyze_right_video(data_path)
    # shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)

def analyze_side_view_video(data_path):
    videos  = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.analyze_videos(this_computer['side_view_config'],videos,shuffle=2, save_as_csv=True )
    deeplabcut.filterpredictions(this_computer['side_view_config'],videos,shuffle=2, save_as_csv=True )

def analyze_eye_video(data_path):
    eye_videos = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('EYE.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.analyze_videos(this_computer['eye_config'],eye_videos,shuffle=1, save_as_csv=True )
    deeplabcut.filterpredictions(this_computer['eye_config'],eye_videos,shuffle=1)

def analyze_top_view_video(data_path):
    text_files = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('video.mp4') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.analyze_videos(this_computer['head_config'],text_files,shuffle=1, save_as_csv=True )
    deeplabcut.filterpredictions(this_computer['head_config'],text_files)

def analyze_left_video(data_path):
    XfilesL = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mask')  ] # find all files with R.avi as file name
    deeplabcut.analyze_videos(this_computer['top_view_config'],XfilesL,shuffle=1, save_as_csv=True)
    deeplabcut.filterpredictions(this_computer['top_view_config'],XfilesL,shuffle=1)

def analyze_right_video(data_path):
    XfilesR = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mirror')  ] # find all files with R.avi as file name
    deeplabcut.analyze_videos(this_computer['top_view_config'],XfilesR,shuffle=1, save_as_csv=True)
    deeplabcut.filterpredictions(this_computer['top_view_config'],XfilesR,shuffle=1)