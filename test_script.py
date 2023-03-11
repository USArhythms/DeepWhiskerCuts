from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.lib.pipeline import analyze_videos
from DeepWhiskerCuts.setting.dlc_setting import eye_shuffle
import os
dir = r'C:\sidevideos\ar37motor\2023_02_22'
manager = ExperimentManager(dir,'side')
for triali in manager.trials:
    if not triali.finished:
        triali.print_progress()
        eye_videos = [os.path.join(manager.dir,triali.name+'EYE.avi')]
        print('undone') 
print('done')