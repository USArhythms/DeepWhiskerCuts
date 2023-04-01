from DeepWhiskerCuts.lib.MovieTools import make_movie_for_all_trials,extract_eye_videos
import deeplabcut
import os
from DeepWhiskerCuts.lib.top_view_spliter import split_left_and_right_from_top_video
from DeepWhiskerCuts.setting.setting import this_computer
from tqdm import tqdm
import pdb

def processs_side_view_data(data_path):
    make_movie_for_all_trials(data_path,parallel=False,ncores = 4)
    analyze_side_view_video(data_path)
    extract_eye_videos(data_path,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle1_271000')
    analyze_eye_video(data_path)
    # shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)

def processs_top_view_data(data_path):
    make_movie_for_all_trials(data_path,parallel=False,ncores = 16)
    analyze_top_view_video(data_path)
    split_left_and_right_from_top_video(data_path)
    analyze_left_video(data_path)
    analyze_right_video(data_path)
    #shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)

def analyze_side_view_video(data_path):
    videos  = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    def deeplabcut_function(video):
        deeplabcut.analyze_videos(this_computer['side_view_config'],[video],shuffle=2, save_as_csv=True )
        deeplabcut.filterpredictions(this_computer['side_view_config'],[video],shuffle=2, save_as_csv=True )
    run_dlc_with_error_handling(videos,deeplabcut_function)

def analyze_eye_video(data_path):
    eye_videos = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('EYE.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    def deeplabcut_function(video):
        deeplabcut.analyze_videos(this_computer['eye_config'],[video],shuffle=1, save_as_csv=True )
        deeplabcut.filterpredictions(this_computer['eye_config'],[video],shuffle=1)
    run_dlc_with_error_handling(eye_videos,deeplabcut_function)

def analyze_top_view_video(data_path):
    text_files = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('video.mp4') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    def deeplabcut_function(video):
        deeplabcut.analyze_videos(this_computer['head_config'],[video],shuffle=1, save_as_csv=True )
        deeplabcut.filterpredictions(this_computer['head_config'],[video])
    run_dlc_with_error_handling(text_files,deeplabcut_function)

def analyze_left_video(data_path):
    XfilesL = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mask')  ] # find all files with R.avi as file name
    def deeplabcut_function(video):
        deeplabcut.analyze_videos(this_computer['top_view_config'],[video],shuffle=1, save_as_csv=True)
        deeplabcut.filterpredictions(this_computer['top_view_config'],[video],shuffle=1)
    run_dlc_with_error_handling(XfilesL,deeplabcut_function)

def analyze_right_video(data_path):
    XfilesR = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.startswith('Mirror')  ] # find all files with R.avi as file name
    def deeplabcut_function(video):
        deeplabcut.analyze_videos(this_computer['top_view_config'],[video],shuffle=1, save_as_csv=True)
        deeplabcut.filterpredictions(this_computer['top_view_config'],[video],shuffle=1)
    run_dlc_with_error_handling(XfilesR,deeplabcut_function)

def run_dlc_with_error_handling(videos,deeplabcut_function):
    for videoi in tqdm(range(len(videos)),'processing videos'): 
        video = videos[videoi]
        try:
            deeplabcut_function(video)
        except BaseException as ex:
            ...
            # log_error(os.path.join(video.split(os.sep)[:-2]),'Error during dlc for: '+video,ex)