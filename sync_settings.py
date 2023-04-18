from DeepWhiskerCuts.setting.setting import common_cache,computers
import os
import shutil
from DeepWhiskerCuts.lib.remote_utility import run_python_script_on_all_servers
path_to_setting_file = os.path.join(os.path.abspath(os.path.curdir),'DeepWhiskerCuts','setting','setting.py')
shutil.copy(path_to_setting_file,common_cache)
run_python_script_on_all_servers('sync_settings.py')
