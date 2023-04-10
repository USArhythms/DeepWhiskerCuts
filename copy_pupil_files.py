from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.setting.setting import this_computer

dir = r'D:\Sidevideos\ar37motor\2023_02_22_ 163949'
manager = ExperimentManager(dir,mode = 'side')
manager.copy_files_for_pupil_qc(this_computer['pupil_destination'])