from ProgressManager import ExperimentManager
import deeplabcut
from setting import this_computer
import numpy as np
# dir = r'D:\Sidevideos\ar37motor\2023_02_22_ 163949'
# manager = ExperimentManager(dir,'side')
# for i in manager.trials:
#     if not i.finished:
#         i.print_progress()
#         shuffle = 3
#         videos = i.get_files_containing_substring('EYE.avi')
#         for video in videos:
#             deeplabcut.analyze_videos(this_computer['eye_config'],[video],shuffle=shuffle, save_as_csv=True )
#             deeplabcut.filterpredictions(this_computer['eye_config'],[video],shuffle=shuffle, save_as_csv=True )
#             print('')
# print()

import re
import os


dir = r'D:\Sidevideos\ar37motor\2023_02_22_ 163949'
files = os.listdir(dir)

trials = []
for filei in files:
    try:
        int(filei)
        trials.append(filei)
    except:
        continue

for triali in trials:
    t1 = [i for i in files if triali in i]

shuffle = 2
avi = re.compile(str(triali)+r'.avi')
mp4 = re.compile(str(triali)+r'video.mp4')
dlc_csv = re.compile(str(triali)+rf'DLC_\w+shuffle{shuffle}_\d+.csv')
dlc_filtered_csv = re.compile(str(triali)+rf'DLC_\w+shuffle{shuffle}_\d+_filtered.csv')
eye_avi = re.compile(str(triali)+r'EYE.avi')
dlc_h5 = re.compile(str(triali)+rf'DLC_\w+shuffle{shuffle}_\d+.h5')
dlc_pickle = re.compile(str(triali)+rf'DLC_\w+shuffle{shuffle}_\w+.pickle')

dlc_file = [i for i in files if re.match(dlc_pickle, i)!=None]

