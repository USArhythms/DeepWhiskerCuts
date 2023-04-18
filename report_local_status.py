
from DeepWhiskerCuts.setting.setting import common_cache,this_computer,computers
from DeepWhiskerCuts.lib.StatusMonitor import StatusMonitor
from DeepWhiskerCuts.lib.remote_utility import run_python_script
monitor = StatusMonitor()
for computer in computers:
    run_python_script(this_computer,'find_status.py')