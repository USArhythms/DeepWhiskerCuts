
from DeepWhiskerCuts.setting.setting import common_cache,this_computer,computers
from DeepWhiskerCuts.lib.StatusMonitor import StatusMonitor,load_common_trials
from DeepWhiskerCuts.lib.remote_utility import run_python_script
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

for animal in common_trials:
    trials = common_trials[animal]
    for triali in trials:
        for computer in computers:
            print(f'computer: {computer}')
            manager = status[computer][animal][triali]
            status = manager.print_progress()
            # pdb.set_trace()
