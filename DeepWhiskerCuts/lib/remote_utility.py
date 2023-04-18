from paramiko.client import SSHClient
from paramiko import AutoAddPolicy
from DeepWhiskerCuts.setting.setting import computers
import os
from time import sleep
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from multiprocessing import Pool
import pdb

def run_python_script_on_all_servers(python_script,computers=computers):
    for computeri in computers:
        config = computers[computeri]
        run_python_script(config,python_script)

def run_command_on_server(server_config,cmd):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(server_config['ip'], username=server_config['user'], password=server_config['pwd'])
    stdin, stdout, stderr = client.exec_command(cmd)
    stdout, stderr = stdout.read().decode(), stderr.read().decode()
    client.close()
    return stdin, stdout, stderr

def get_folders(folders):
    if len(folders)>2:
        folders = folders[:-2]
        folders = folders.split(',')  
        folders[0] = folders[0][1:]
        folders[-1] = folders[-1][:-1]
        return folders
    else:
        return []

def get_animal_folders_from_server(server_config):
    _, folders, _ = run_python_script(server_config,'list_available_animal_folders.py')
    if len(folders)>2:
        folders = eval(folders[:-2])
    else:
        folders = []
    # pdb.set_trace()
    return folders

def get_trial_folders_from_server(server_config,animal_folder):
    animal_folder = os.path.join(server_config['data_path'],animal_folder)
    _, folders, _ = run_python_script(server_config,f'list_available_trial_folders.py  "{animal_folder}"')
    return get_folders(folders)

def run_python_script(server_config,python_script_command):
    return run_command_on_server(server_config,f"conda activate {server_config['dlc_environment']} && python {os.path.join(server_config['code_path'],python_script_command)}")

def process_folder_on_server(server_config,folder,trial):
    stdin, folders, stderr = run_python_script(server_config,f'process_experiment.py --folder "{folder}" --trial "{trial}"')
    print(folders)
    return stdin, folders, stderr

def pick_folder(folders,prompt):
    for i in range(len(folders)):
        print(f'{i+1}. {folders[i]}')
    sleep(0.01)
    folder = input(prompt)
    while int(folder)>len(folders):
        print('invalid number')
        folder = input(prompt)
    folder = folders[int(folder)-1]
    print(f'==================picked: {folder}====================')
    return folder

def start_remote_trials(computers=computers):
    choices = []
    for name,config in computers.items():
        print(f'=================={name}====================')
        files = get_animal_folders_from_server(config)
        animal = pick_folder(files,'Pick an animal\n')
        trials = get_trial_folders_from_server(config,animal)
        trial = pick_folder(trials,'Pick a trial\n')
        choices.append((animal,trial))
    i=0

    with Pool(processes=4) as pool:
        futures = []
        for name,config in computers.items():
            print(f'===============processing {name} for animal: {animal} trial: {trial}==================')
            animal,trial = choices[i]
            future = pool.apply_async(process_folder_on_server, (config, animal, trial))
            futures.append(future)
        
            finished = False
        while not finished:
            status = [i.ready() for i in futures]
            finished = np.all(status)
            print(f'{sum(status)}/{len(status)} finished')
            sleep(10)

        for i in range(3):
            print(f'============result of {names[i]}=============')
            if futures[i].successful():
                print('process successfu:')
            else:
                print('An exception occured:')
            print(futures[i].get())


def start_process_with_concurrent_future(computers,choices,names):
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = []
        for name,config in computers.items():
            print(f'===============processing {name} for animal: {animal} trial: {trial}==================')
            animal,trial = choices[i]
            future = executor.submit(process_folder_on_server,config, animal, trial)
            futures.append(future)
            i+=1
    
    finished = False
    while not finished:
        status = [i.done() for i in futures]
        finished = np.all(status)
        print(f'{sum(status)}/{len(status)} finished')
        sleep(1)

    for i in range(3):
        print(f'============result of {names[i]}=============')
        try:
            print(futures[i].result())
        except:
            print(futures[i].exception())
