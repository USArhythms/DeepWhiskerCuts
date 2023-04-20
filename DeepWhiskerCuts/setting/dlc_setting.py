import os

windows_dlc_folder = r'\\dk-server.dk.ucsd.edu\afassihizakeri\DLC'
linux_dlc_folder = '/net/dk-server/afassihizakeri/DLC/'

side_view_config_name = 'SideviewLeft_Feb2022'
side_view_time_stamp = '-Arash-2022-02-08'
side_view_config_file = os.path.join(side_view_config_name+side_view_time_stamp,'config.yaml')
side_view_shuffle = 2
eye_config_file = os.path.join('Eye 482_EPL-Arash-2022-05-24','config.yaml')
eye_shuffle = 3
whisker_config_file = os.path.join('ar30shiwker-Arash-2021-09-13','config.yaml')
left_shuffle = 1
right_shuffle = 1
top_view_config_name = 'Topview3435-Arash-2021-07-28'
top_view_config_file = os.path.join(top_view_config_name,'config.yaml')
top_shuffle = 1

windows_side_view = os.path.join(windows_dlc_folder,side_view_config_file)
windows_eye = os.path.join(windows_dlc_folder,eye_config_file)
windows_top_view = os.path.join(windows_dlc_folder,top_view_config_file)
windows_whisker = os.path.join(windows_dlc_folder,whisker_config_file)

windows_dlc_config = dict()
windows_dlc_config['side_view_config'] = windows_side_view
windows_dlc_config['eye_config'] = windows_eye
windows_dlc_config['top_view_config'] = windows_top_view
windows_dlc_config['whisker_config'] = windows_whisker
windows_dlc_config['pupil_destination'] = r'\\dk-server.dk.ucsd.edu\afassihizakeri\pupil_tracking'