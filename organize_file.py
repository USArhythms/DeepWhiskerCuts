from DeepWhiskerCuts.setting.setting import leftcam1,pupil_destination
# from DeepWhiskerCuts.lib.ProgressManager import ProgressManager
import pdb
import os
import shutil
from dirsync import sync

animals = os.listdir(leftcam1['data_path'])

for animali in animals:
    experiments = os.listdir(os.path.join(leftcam1['data_path'],animali))
    print(animali)
    for experimenti in experiments:
        experiment_folder = os.path.join(leftcam1['data_path'],animali,experimenti)
        nfiles = len(os.listdir(experiment_folder))
        print('    ' + experimenti)
        print('    '+str())
        if nfiles > 30:
            destination_folder = os.path.join(pupil_destination,leftcam1['tag'],*experiment_folder.split(os.path.sep)[-2:])
            os.makedirs(destination_folder,exist_ok=True)
            print('copying')
            sync(experiment_folder, destination_folder, 'sync')

        # manager = ProgressManager(experiment_folder,'side')
        # if manager.finished:
        #     destination_folder = os.path.join(pupil_destination,leftcam1['tag'],*manager.dir.split(os.path.sep)[-2:])
        #     os.makedirs(destination_folder,exist_ok=True)
        #     print('copying')
        #     sync(experiment_folder, destination_folder, 'sync')