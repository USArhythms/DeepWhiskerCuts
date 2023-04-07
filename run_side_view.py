from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
from DeepWhiskerCuts.lib.pipeline import processs_side_view_data
dir = r'D:\Sidevideos\ar37\2023_03_23_ 182402'
processs_side_view_data(dir)
manager = ExperimentManager(dir,'side')
for triali in manager.trials:
    if not triali.finished:
        # pdb.set_trace()
        manager.fix_trial(triali)
print('done')