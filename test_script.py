from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.lib.pipeline import analyze_videos
from DeepWhiskerCuts.setting.dlc_setting import eye_shuffle
import os
dir = r'D:\Sidevideos\ar37motor\2023_02_22_ 163949'
manager = ExperimentManager(dir,'side')
for triali in manager.trials:
    if not triali.finished:
        triali.fix_trial()
print('done')