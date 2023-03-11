from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.lib.pipeline import analyze_videos
from DeepWhiskerCuts.setting.dlc_setting import eye_shuffle
import os
import pdb
dir = r'D:\Sidevideos\ar37motor\2023_02_22'
manager = ExperimentManager(dir,'side')
for triali in manager.trials:
    if not triali.finished:
        # pdb.set_trace()
        triali.print_progress()
        eye_videos = [os.path.join(manager.dir,triali.name+'EYE.avi')]
        analyze_videos(eye_videos,'eye_config',shuffle=eye_shuffle)
        print('undone') 
print('done')