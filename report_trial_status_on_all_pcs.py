
from DeepWhiskerCuts.setting.setting import common_cache,computers
from DeepWhiskerCuts.lib.StatusMonitor import load_common_trials
from DeepWhiskerCuts.lib.remote_utility import pick_folder
import pickle
import os
import pdb

common_trials = load_common_trials()
files = os.listdir(common_cache)
status_files = [i for i in files if '.status' in i]
computers = [i.split('.status')[0] for i in status_files]
status = {}
for computer in computers:
    status[computer] = pickle.load(open(os.path.join(common_cache,f'{computer}.status'),'rb'))

animals = list(common_trials.keys())
animal = pick_folder(animals,'pick an animal')
trials = common_trials[animal]
triali = pick_folder(list(trials),'pick an animal')
for computer in computers:
    try:
        print(f'computer: {computer}')
        manager = status[computer][animal][triali]
        manager.print_progress()
    except:
        pdb.set_trace()
