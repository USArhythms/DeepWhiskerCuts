from DeepWhiskerCuts.setting.setting import common_cache
import os
import shutil

path_to_setting_file = os.path.join(common_cache,'setting.py')
local_settings_folder = os.path.join(os.path.abspath(os.path.curdir),'DeepWhiskerCuts','setting')
shutil.copy(path_to_setting_file,local_settings_folder)
