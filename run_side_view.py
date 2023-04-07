from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.lib.pipeline import processs_side_view_data
from folder_to_process import side_folder

processs_side_view_data(side_folder)
manager = ExperimentManager(side_folder,'side')
for triali in manager.trials:
    if not triali.finished:
        manager.fix_trial(triali)
print('done')