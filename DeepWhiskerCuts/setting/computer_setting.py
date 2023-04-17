import os
from DeepWhiskerCuts.setting.dlc_setting import side_view_config_file,eye_config_file,top_view_config_file,head_config_file

data_root = ''
windows_dlc_folder = r'\\dk-server.dk.ucsd.edu\afassihizakeri\DLC'
linux_dlc_folder = '/net/dk-server/afassihizakeri/DLC/'

side_view_computer_right = dict()
side_view_computer_left = dict()
top_view_computer = dict()
pons = dict()
arash = dict()
side_view_computer_mid = dict()

side_view_computer_left['ip'] = '132.239.77.79'
side_view_computer_left['user'] = 'DKLAb'
side_view_computer_left['pwd'] = 'Pw4dklab'
side_view_computer_left['data_path'] = r'D:\Sidevideos'
side_view_computer_left['code_path'] = r'C:\Users\DKLAb\DeepLabCut'
side_view_computer_left['side_view_config'] = os.path.join(windows_dlc_folder,side_view_config_file)
side_view_computer_left['eye_config'] = os.path.join(windows_dlc_folder,eye_config_file)

side_view_computer_right['ip'] = '132.239.185.135'
side_view_computer_right['user'] = 'dklab'
side_view_computer_right['pwd'] = 'Pw4dklab'
side_view_computer_right['data_path'] = r'D:\Sidevideos'
side_view_computer_right['code_path'] = r'C:\Users\dklab\DeepWhiskerCuts'
side_view_computer_right['side_view_config'] = os.path.join(windows_dlc_folder,side_view_config_file)
side_view_computer_right['eye_config'] = os.path.join(windows_dlc_folder,eye_config_file)
side_view_computer_right['pupil_destination'] = r'\\dk-server.dk.ucsd.edu\afassihizakeri\pupil_tracking'
side_view_computer_right['tag'] = r'right_cam1'
side_view_computer_right['top_view_config'] = os.path.join(windows_dlc_folder,top_view_config_file)
side_view_computer_right['head_config'] = os.path.join(windows_dlc_folder,head_config_file)
side_view_computer_right['ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe'

side_view_computer_mid['ip'] = '132.239.185.182'
side_view_computer_mid['user'] = 'dklab'
side_view_computer_mid['pwd'] = 'Pw4dklab'
side_view_computer_mid['data_path'] = r'C:\Sidevideos'
side_view_computer_mid['code_path'] = r'C:\Users\dklab\DeepWhiskerCuts'
side_view_computer_mid['side_view_config'] = os.path.join(windows_dlc_folder,side_view_config_file)
side_view_computer_mid['eye_config'] = os.path.join(windows_dlc_folder,eye_config_file)
side_view_computer_mid['top_view_config'] = os.path.join(windows_dlc_folder,top_view_config_file)
side_view_computer_mid['head_config'] = os.path.join(windows_dlc_folder,head_config_file)
side_view_computer_mid['ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe'
side_view_computer_mid['dlc_environment'] = 'conda actiavte deeplabcut'

pons['side_view_config'] = os.path.join(linux_dlc_folder,side_view_config_file)
pons['eye_config'] = os.path.join(linux_dlc_folder,eye_config_file)

top_view_computer['ip'] = '132.239.185.175'
top_view_computer['user'] = 'Tennessee'
top_view_computer['pwd'] = 'Pw4dklab'
top_view_computer['data_path'] = r'D:\Sidevideos'
top_view_computer['code_path'] = r'C:\Users\Tennessee\DeepWhiskerCuts'
top_view_computer['top_view_config'] = os.path.join(windows_dlc_folder,top_view_config_file)
top_view_computer['head_config'] = os.path.join(windows_dlc_folder,head_config_file)
