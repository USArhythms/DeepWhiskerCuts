import os
import re
from setting.setting import this_computer,side_view_shuffle,eye_shuffle,left_shuffle,right_shuffle,top_shuffle

def get_trial(dir):
    files = os.listdir(dir)
    trials = []
    for filei in files:
        try:
            int(filei)
            trials.append(filei)
        except:
            continue

class Trial:
    def __init__(self,triali):
        avi = re.compile(str(triali)+r'.avi')
        mp4 = re.compile(str(triali)+r'video.mp4')
        dlc_csv = re.compile(str(triali)+rf'DLC_\w+shuffle{side_view_shuffle}_\d+.csv')
        dlc_filtered_csv = re.compile(str(triali)+rf'DLC_\w+shuffle{side_view_shuffle}_\d+_filtered.csv')
        dlc_h5 = re.compile(str(triali)+rf'DLC_\w+shuffle{side_view_shuffle}_\d+.h5')
        dlc_pickle = re.compile(str(triali)+rf'DLC_\w+shuffle{side_view_shuffle}_\w+.pickle')
        dlc_checks = [dlc_csv,dlc_filtered_csv,dlc_h5,dlc_pickle]
        eye_avi = re.compile(str(triali)+r'EYE.avi')
        eye_dlc_csv = re.compile(str(triali)+rf'DLC_\w+shuffle{eye_shuffle}_\d+.csv')
        eye_dlc_filtered_csv = re.compile(str(triali)+rf'DLC_\w+shuffle{eye_shuffle}_\d+_filtered.csv')
        eye_dlc_h5 = re.compile(str(triali)+rf'DLC_\w+shuffle{eye_shuffle}_\d+.h5')
        eye_dlc_pickle = re.compile(str(triali)+rf'DLC_\w+shuffle{eye_shuffle}_\w+.pickle')
        eye_dlc_checks = [eye_dlc_csv,eye_dlc_filtered_csv,eye_dlc_h5,eye_dlc_pickle]
        self.side_view_check_list = [[avi],[mp4],dlc_checks,[eye_avi],eye_dlc_checks]

class SideviewTrial(Trial):
    def __init__(self,triali):
        super().__init__(triali)
        self.check_list = self.side_view_check_list
        self.side_view_tasks = ['has_full_resolution_video','has_downsampled_video','has_dlc_output',\
        'has_eye_video','has_eye_dlc_output']
        self.checks = []
        for checki in self.checks

class PreProcess:
    def __init__(self,dir):
        self.dir = dir
        trials = get_trial(dir)
        shuffle = 2
        
class SideViewProcess:
    def __init__(self,dir):
        self.dir = dir
        trials = get_trial(dir)
        
        ...

class TopViewProcess:
    def __init__(self,dir):
        self.dir = dir
        trials = get_trial(dir)