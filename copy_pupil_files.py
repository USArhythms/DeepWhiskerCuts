from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.setting.setting import this_computer

dir = r'C:\sidevideos\ar37motor\2023_02_22'
manager = ExperimentManager(dir,mode = 'side')
manager.copy_files_for_pupil_qc(this_computer['pupil_destination'])