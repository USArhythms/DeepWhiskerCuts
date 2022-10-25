from MovieTools import make_movie_and_stimulus_file,save_trial_n,extract_eye_videos
import re
import deeplabcut
import os
import shutil
from top_view_spliter import split_left_and_right_from_top_video

def processs_side_view_data(data_path):
    side_view_config_file ='/data/SideviewLeft_Feb2022-Arash-2022-02-08/config.yaml';
    eye_config_file ='/data/EyeAug22-A-2022-08-03/config.yaml';
    # destination='/net/dk-server/afassihizakeri/SC_Movies/ar32motor/2021_08_02/Side'

    make_movie_and_stimulus_file(data_path,parallel=True,ncores = 16)
    save_trial_n(data_path)
    videos  = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.analyze_videos(side_view_config_file,videos,shuffle=1, save_as_csv=True )
    extract_eye_videos(data_path,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle1_271000')
    eye_videos = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('EYE.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.filterpredictions(eye_config_file,eye_videos,shuffle=2)
    # shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)

def processs_top_view_data(data_path):
    top_view_config_file ='\\dk-server.dk.ucsd.edu\afassihizakeri\DLC\WhiskerMuscimol-xx-2022-10-10\config.yaml';
    head_config_file ='\\dk-server.dk.ucsd.edu\afassihizakeri\DLC\SC_Muscimol_2019-Arash_2-2022-10-03\config.yaml';
    # destination='/net/dk-server/afassihizakeri/SC_Movies/ar32motor/2021_08_02/Side'

    # make_movie_and_stimulus_file(data_path,parallel=True,ncores = 16)
    # save_trial_n(data_path)

    text_files = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('video.mp4') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    deeplabcut.analyze_videos(head_config_file,text_files,shuffle=1, save_as_csv=True )
    deeplabcut.filterpredictions(head_config_file,text_files)

    split_left_and_right_from_top_video(data_path)

    XfilesL = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mask')  ] # find all files with R.avi as file name
    XfilesR = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mirror')  ] # find all files with R.avi as file name
    deeplabcut.analyze_videos(top_view_config_file,XfilesL,shuffle=1, save_as_csv=True)
    deeplabcut.filterpredictions(top_view_config_file,XfilesL,shuffle=1)
    deeplabcut.analyze_videos(top_view_config_file,XfilesR,shuffle=1, save_as_csv=True)
    deeplabcut.filterpredictions(top_view_config_file,XfilesR,shuffle=1)
    # shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)
