from ProgressManager import ExperimentManager
import deeplabcut
from setting import this_computer
import numpy as np
dir = r'D:\Sidevideos\ar37motor\2023_02_22_ 163949'
manager = ExperimentManager(dir,'side')
for i in manager.trials:
    if not i.finished:
        i.print_progress()
        shuffle = 3
        videos = i.get_files_containing_substring('EYE.avi')
        for video in videos:
            deeplabcut.analyze_videos(this_computer['eye_config'],[video],shuffle=shuffle, save_as_csv=True )
            deeplabcut.filterpredictions(this_computer['eye_config'],[video],shuffle=shuffle, save_as_csv=True )
            print('')
print()