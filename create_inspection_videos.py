import os
import random
from deeplabcut import create_labeled_video
from setting import this_computer
dir = r'D:\Sidevideos\ar37motor\2023_02_22_ 163949'
eye_videos = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith('EYE.avi') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
videos =  random.sample(eye_videos,10)
create_labeled_video(this_computer['eye_config'],videos,shuffle = 3)
print()