from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.lib.pipeline import processs_side_view_data
from folder_to_process import side_folder
from DeepWhiskerCuts.setting.setting import this_computer

processs_side_view_data(side_folder)
manager = ExperimentManager(side_folder,'side')
for triali in manager.trials:
    if not triali.finished:
        manager.fix_trial(triali)
manager.copy_files_for_pupil_qc(this_computer['pupil_destination'])
print('done')