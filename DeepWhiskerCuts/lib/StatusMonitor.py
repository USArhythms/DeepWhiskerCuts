from DeepWhiskerCuts.lib.remote_utility import get_animal_folders_from_server,get_trial_folders_from_server
from DeepWhiskerCuts.setting.setting import computers,this_computer,common_cache
from DeepWhiskerCuts.lib.ProgressManager import ExperimentManager
import pickle
import pdb
import os

class StatusMonitor:
    def __init__(self,computers=computers):
        self.computers = computers
        self.animals = self.get_animal_folders_on_remote_computer()
        self.common_animals = self.get_common_animals()
        self.trials = self.get_trials_from_remote_computer()
        self.common_trials = self.get_common_trials()
        save_common_trials(self.common_trials)

    def get_animal_folders_on_remote_computer(self):
        animals = {}
        for computeri in self.computers:
            config = self.computers[computeri]
            animals[computeri] = get_animal_folders_from_server(config)
        return animals

    def get_common_animals(self):
        animals_lower_case = dict(zip(self.computers.keys(),[[i.lower() for i in self.animals[computeri]] for computeri in self.computers]))
        return eval( '&'.join([f'set({animals_lower_case[i]})' for i in self.computers]))

    def get_trials_from_remote_computer(self):
        trials = dict(zip(self.computers,[{} for _ in range(len(self.computers))]))
        for computeri in self.computers: 
            config = self.computers[computeri]
            for animal in self.common_animals:
                animal_key = [i for i in self.animals[computeri] if i.lower() == animal][0]
                trials[computeri][animal] = get_trial_folders_from_server(config,animal_key)
                trials[computeri][animal] = ['_'.join(i.split('_')[:3]) if len(i.split('_'))>3 else i for i in trials[computeri][animal]]
        return trials

    def get_common_trials(self):
        common_trials = {}
        for animal in self.common_animals:
            common_trials[animal] = eval( '&'.join([f'set({self.trials[i][animal]})' for i in self.computers]))
        return common_trials

def save_common_trials(common_trials):
    pickle.dump(common_trials,open(os.path.join(common_cache,'common_trials.pkl'),'wb'))

def load_common_trials():
    return pickle.load(open(os.path.join(common_cache,f'common_trials.pkl'),'rb'))

def get_current_pc_status():
    common_trials = load_common_trials()
    status = dict(zip(common_trials.keys(),[{} for _ in range(len(common_trials))]))
    for animali in common_trials:
        trials = common_trials[animali]
        if len(trials)>0:
            for triali in trials:
                animal_folder = os.path.join(this_computer['data_path'],animali)
                # pdb.set_trace()
                folders = os.listdir(animal_folder)
                trial_folder = os.path.join(animal_folder,[i for i in folders if triali in i][0])
                manager = ExperimentManager(trial_folder,this_computer['mode'])
                status[animali][triali] = manager
    return status