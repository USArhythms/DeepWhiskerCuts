
from MovieTools import make_movie_and_stimulus_file,save_trial_n,extract_eye_videos
from glob import glob
import deeplabcut
import os
import shutil

data_path = '/data/2022_07_28'

make_movie_and_stimulus_file(data_path,parallel=True,ncores = 4)

# path_config_file ='/data/config.yaml';
# videos = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
# print(videos[1])
# temp1=deeplabcut.analyze_videos(path_config_file,videos,shuffle=1, save_as_csv=True )
# temp=deeplabcut.filterpredictions(path_config_file,videos)