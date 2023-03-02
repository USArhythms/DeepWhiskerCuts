from ProgressManager import ExperimentManager
import numpy as np
dir = r'D:\Sidevideos\ar37motor\2023_02_22_ 163949'
manager = ExperimentManager(dir,'side')
manager.trials[0].print_progress()

np.sum([i.finished for i in manager.trials])

np.sum([not i.finished for i in manager.trials])

for i in manager.trials:
    if not i.finished:
        i.print_progress()
        print('')

print()