import os
import numpy as np

class ProgressBase:
    def __init__(self,dir,mode,check_filtered=True):
        self.dir = dir
        self.mode = mode
        self.side_view_tasks = ['has_full_resolution_video','has_downsampled_video','has_dlc_output',\
            'has_filtered_dlc_output','has_eye_video','has_eye_dlc_output','has_filtered_eye_dlc_output']

        self.top_view_tasks = ['has_full_resolution_video','has_downsampled_video','has_topview_overall_dlc_output',\
            'has_filtered_overall_topview_dlc_output','has_left_video','has_right_video','has_topview_left_dlc_output',\
                'has_filtered_topview_left_dlc_output','has_topview_right_dlc_output','has_filtered_topview_right_dlc_output']
        if mode=='top':
            self.tasks = self.top_view_tasks
        if mode == 'side':
            self.tasks = self.side_view_tasks
        self.check_filtered = check_filtered
        
    def get_printable_task_name(self,task_attribute):
        return ' '.join(task_attribute[4:].split('_'))
    
    def is_trial_folder(self,folder_name):
        has_jpg = os.path.exists(os.path.join(self.dir,folder_name,'0.jpg'))
        has_png = os.path.exists(os.path.join(self.dir,folder_name,'0.png'))
        has_jpeg = os.path.exists(os.path.join(self.dir,folder_name,'0.jpeg'))
        return has_jpg or has_png or has_jpeg
    
    def get_folders_in_path(self,dir):
        return [ f.path for f in os.scandir(dir) if f.is_dir() ]
    
    def check_unfinished_tasks(self):
        unfinished_tasks = self.get_unfinished_tasks()
        for itemi,report in unfinished_tasks.items():
            if len(report)>0:
                print(f'{itemi.type} {itemi.name}')
                itemi.print_unfinished_tasks(report)
    
    def get_unfinished_tasks(self):
        report = {}
        for itemi in getattr(self,self.list_attribute):
            tasks = itemi.get_unfinished_tasks()
            if len(tasks) == 0:
                continue
            report[itemi] = tasks
        return report
    
    def get_item_list(self):
        return getattr(self,self.list_attribute)
    
    def print_progress_brief(self,show_finished = False):
        for item in self.get_item_list():
            if item.finished:
                if not show_finished:
                    continue
                symbol = '#'
            else:
                symbol = 'X'
            print(f'{item.name}: {symbol}')
        
    def get_next_step_text(self,function):
        return 'need ' + ' '.join(function.split('_')[1:])

class ProgressManager(ProgressBase):
    def __init__(self,dir,mode,check_filtered = True):
        super().__init__(dir,mode,check_filtered)
        self.animal_folders = self.get_folders_in_path(dir)
        self.check_animal_folders()
        self.animals = [AnimalManager(i,self.mode) for i in self.animal_folders]
        self.list_attribute = 'animals'
        self.finished = np.all([i.finished for i in getattr(self,self.list_attribute)])

    def check_animal_folders(self):
        nfolders = len(self.animal_folders)
        delete = []
        for i in range(nfolders):
            folder = self.animal_folders[i]
            subfolders = self.get_folders_in_path(folder)
            if len(subfolders)==0:
                delete.append(i)
                continue
            trial_folder = os.path.basename(folder) + os.sep + os.path.basename(subfolders[0]) + os.sep + '0'
            if not self.is_trial_folder(trial_folder):
                delete.append(i)
        delete.sort(reverse=True)
        for i in delete:
            del self.animal_folders[i]

    def get_animal_folders_through_search(self):
        folders_to_search = self.get_folders_in_path(self.dir)
        animal_folder = []
        while folders_to_search != []:
            folder = folders_to_search.pop()
            sub_folders = self.get_folders_in_path(folder)
            folders_to_search = folders_to_search+sub_folders
            for folderi in sub_folders:
                if self.is_trial_folder(os.path.basename(folderi)):
                    animal_folderi = os.path.normpath(folderi + os.sep + os.pardir)
                    animal_folder.append(animal_folderi)
                    folders_to_search = [i for i in folders_to_search if animal_folderi not in i]
                    break

    def print_project_brief(self):
        if self.finished:
            print('all done')
            return
        for animal in self.animals:
            if animal.finished:
                continue
            print(animal.name)
            for experiment in animal.experiments:
                if experiment.finished:
                    continue
                print(f'{experiment.name}: {experiment.get_next_step()}')

class AnimalManager(ProgressBase):
    def __init__(self,dir,mode,check_filtered = True):
        super().__init__(dir,mode,check_filtered)
        self.experiment_folders = self.get_folders_in_path(dir)
        self.check_experiment_folders()
        self.experiments = [ExperimentManager(i,self.mode) for i in self.experiment_folders]
        self.name = os.path.basename(dir)
        self.type = 'animal'
        self.list_attribute = 'experiments'
        self.finished = np.all([i.finished for i in getattr(self,self.list_attribute)])
    
    def print_progress(self):
        print(f'progress for animal {self.name}')
        for experiment in self.experiments:
            experiment.print_progress()
    
    def check_experiment_folders(self):
        nfolders = len(self.experiment_folders)
        delete = []
        for i in range(nfolders):
            folder = self.experiment_folders[i]
            trial_folder = os.path.basename(folder) + os.sep + '0'
            if not self.is_trial_folder(trial_folder):
                delete.append(i)
        delete.sort(reverse=True)
        for i in delete:
            del self.experiment_folders[i]

class ExperimentManager(ProgressBase):
    def __init__(self,dir,mode,check_filtered = True):
        super().__init__(dir,mode,check_filtered)
        self.all_files = os.listdir(dir)
        self.name = os.path.basename(dir)
        subfolders = self.get_folders_in_path(dir)
        self.trial_names = [os.path.basename(i) for i in subfolders]
        self.non_trial_folders = [i for i in self.trial_names if not self.is_trial_folder(i)]
        self.trial_names = [i for i in self.trial_names if self.is_trial_folder(i)]
        self.trials = [Trial(self.all_files,i,self.mode) for i in self.trial_names]
        self.type = 'experiment'
        self.list_attribute = 'trials'
        self.finished = np.all([i.finished for i in getattr(self,self.list_attribute)])
    
    def print_progress(self):
        print(f'progress for experiment {self.name}')
        for trial in self.trials:
            trial.print_progress()
    
    def check_unfinished_tasks(self):
        unfinished_tasks = self.get_unfinished_tasks()
        self.print_unfinished_tasks(unfinished_tasks)
    
    def print_unfinished_tasks(self,unfinished_tasks):
        for triali,tasks in unfinished_tasks.items():
            print(f'trial: {triali}')
            for taski in tasks:
                print(f'does not have {self.get_printable_task_name(taski)}')
        
    def get_unfinished_tasks(self):
        report = {}
        unfinished_tasks = [i.get_unfinished_tasks() for i in self.trials]
        has_unfinished = [len(i)>0 for i in unfinished_tasks]
        if np.any(has_unfinished):
            for triali in np.where(has_unfinished)[0]:
                report[self.trial_names[triali]] = unfinished_tasks[triali]
        return report
    
    def get_next_step(self):
        if self.finished:
            return 'done'
        task_id = -1
        for triali in self.trials:
            if triali.finished:
                continue
            if task_id < triali.next_task:
                task_id = triali.next_task
        return self.get_next_step_text(self.tasks[task_id])

class Trial(ProgressBase):
    def __init__(self,all_files,trial_name,mode,check_filtered=True):
        super().__init__('',mode,check_filtered)
        self.name = trial_name
        self.all_files = all_files
        self.check_full_resolution_video()
        self.check_downsampled_video()
        self.check_overall_dlc()
        self.check_eye_video()
        self.check_left_video()
        self.check_right_video()
        self.check_eye_dlc()
        self.check_top_view_left_dlc()
        self.check_top_view_right_dlc()
        self.type = 'trial'
        self.task_finished = [getattr(self,taski) for taski in self.tasks]
        self.finished = np.all(self.task_finished)
        if not self.finished:
            self.next_task = np.where(~np.array(self.task_finished))[0][0]
    
    def get_files_containing_substring(self,substring):
        return [i for i in self.all_files if i.split(substring)[0]==self.name and i!= self.name]
    
    def check_full_resolution_video(self):
        files = self.get_files_containing_substring('.avi')
        self.has_full_resolution_video = len(files)==1
    
    def check_eye_video(self):
        files = self.get_files_containing_substring('EYE.avi')
        self.has_eye_video = len(files)==1

    def check_left_video(self):
        files = self.get_files_containing_substring('L.avi')
        self.has_left_video = len(files)==1
    
    def check_right_video(self):
        files = self.get_files_containing_substring('R.avi')
        self.has_right_video = len(files)==1
    
    def check_downsampled_video(self):
        files = self.get_files_containing_substring('video.mp4')
        self.has_downsampled_video = len(files)==1
    
    def check_if_file_combo_exists(self,file_combo,files):
        return np.all([np.all([keyword in i for i in files]) for keyword in file_combo])
    
    def check_overall_dlc(self):
        self.check_dlc_output('DLC','has_dlc_output','has_filtered_dlc_output')
    
    def check_eye_dlc(self):
        self.check_dlc_output('EYEDLC','has_eye_dlc_output','has_filtered_eye_dlc_output')
    
    def check_top_view_left_dlc(self):
        self.check_dlc_output('Mirror','has_topview_left_dlc_output','has_filtered_topview_left_dlc_output')
    
    def check_top_view_right_dlc(self):
        self.check_dlc_output('Mask','has_topview_right_dlc_output','has_filtered_topview_right_dlc_output')

    def check_top_view_overall_dlc(self):
        self.check_dlc_output('DLC_resnet50','has_topview_overall_dlc_output','has_filtered_overall_topview_dlc_output')

    def check_dlc_output(self,dlc_string,dlc_field,filtered_dlc_field):
        files = self.get_files_containing_substring(dlc_string)
        unfiltered = [i for i in files if 'filtered' not in i]
        setattr(self,dlc_field,self.check_if_file_combo_exists(['h5','_meta.pickle','csv'],unfiltered))
        if self.check_filtered:
            filtered = [i for i in files if 'filtered' in i]
            setattr(self,filtered_dlc_field,self.check_if_file_combo_exists(['h5','csv'],filtered))
        else:
            setattr(self,filtered_dlc_field,True)
    
    def print_progress(self):
        print(f'progress for trial {self.name}')
        for taski in self.tasks:
            task_name = self.get_printable_task_name(taski)
            if getattr(self,taski):
                if 'filtered' in task_name and self.check_filtered==False:
                    continue
                print('has '+task_name)
            else:
                print('does not have '+task_name)
    
    def get_unfinished_tasks(self):
        return [taski for taski in self.tasks if not getattr(self,taski)]
    
    def print_unfinished_tasks(self):
        unfinished = self.get_unfinished_tasks()
        print(f'trial {self.name} does not have:')
        [print(i) for i in unfinished]


        
        