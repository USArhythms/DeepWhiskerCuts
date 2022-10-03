from MovieTools import make_movie_and_stimulus_file,save_trial_n,extract_eye_videos
import re
import deeplabcut
import os
import shutil

data_path = '/data/2022_07_28'
side_view_config_file ='/data/SideviewLeft_Feb2022-Arash-2022-02-08/config.yaml';
eye_config_file ='/data/EyeAug22-A-2022-08-03/config.yaml';
destination='/net/dk-server/afassihizakeri/SC_Movies/ar32motor/2021_08_02/Side'

make_movie_and_stimulus_file(data_path,parallel=False,ncores = 4)
save_trial_n(data_path)
videos = [os.path.join(data_path,f) for f in os.listdir(data_path) if re.match(r'[0-9]+.avi', f)]
temp1=deeplabcut.analyze_videos(side_view_config_file,videos,shuffle=1, save_as_csv=True )
extract_eye_videos(data_path,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle1_271000')
eye_videos = [os.path.join(data_path,f) for f in os.listdir(data_path) if re.match(r'[0-9]+EYE.avi', f)]
temp=deeplabcut.filterpredictions(eye_config_file,eye_videos,shuffle=2)
shutil.copytree( data_path,destination, ignore=shutil.ignore_patterns('*.avi'),copy_function = shutil.copy)