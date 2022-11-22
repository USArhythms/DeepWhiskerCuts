import os
from ProgressManager import ProgressManager,ExperimentManager
root_dir = '/net/dk-server/afassihizakeri/rightsidemovies/'
dir = '/net/dk-server/afassihizakeri/rightsidemovies/ar38motor/2022_02_08'
manager = ProgressManager(root_dir)
manager.animals[0].experiments[0].check_unfinished_tasks()
