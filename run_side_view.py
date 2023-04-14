from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.lib.pipeline import processs_side_view_data
from folder_to_process import side_folder
from DeepWhiskerCuts.setting.setting import this_computer
import pdb
side_folder=r'D:\Sidevideos\ar37\2023_03_23_ 182249'
processs_side_view_data(side_folder)
for i in range(100):
    try:
        manager = ExperimentManager(side_folder,'side')
        for triali in manager.trials:
            if not triali.finished:
                print(f'fixing trial {triali.name}')
                triali.print_progress()
                manager.fix_trial(triali)
        manager.copy_files_for_pupil_qc(this_computer['pupil_destination'])
    except:
        ...
print('done')