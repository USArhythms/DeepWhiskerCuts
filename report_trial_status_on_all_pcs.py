
from DeepWhiskerCuts.setting.setting import common_cache,this_computer,computers
from DeepWhiskerCuts.lib.StatusMonitor import load_common_trials
# from DeepWhiskerCuts.lib.StatusMonitor import StatusMonitor,load_common_trials
# from DeepWhiskerCuts.lib.remote_utility import run_python_script,pick_folder
from DeepWhiskerCuts.lib.remote_utility import pick_folder
import pickle
import os
import pdb

# monitor = StatusMonitor()
# for computer in computers:
#     pdb.set_trace()
#     run_python_script(computer,'find_status.py')

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
trial = pick_folder(list(trials),'pick an trial')
for computer in computers:
    try:
        print(f'-------------computer: {computer}---------------')
        manager = status[computer][animal][trial]
        manager.print_progress()
    except:
        pdb.set_trace()
