
import os
from pipeline import processs_side_view_data,analyze_side_view_video,extract_eye_videos,analyze_eye_video
from MovieTools import make_movie_and_stimulus_file
from ProgressManager import ExperimentManager
dir = r'D:\Sidevideos\ar37motor\2023_02_22'
# make_movie_and_stimulus_file(dir,parallel=False,ncores = 6)
# manager = ExperimentManager(dir,mode = 'side')
# manager.copy_full_resolution_videos(r'\\dk-server.dk.ucsd.edu\afassihizakeri\eyemovies\Leftcam1')
#analyze_side_view_video(dir)
# extract_eye_videos(dir,'DLC_resnet50_SideviewLeft_Feb2022Feb8shuffle2_500000_filtered')
analyze_eye_video(dir)