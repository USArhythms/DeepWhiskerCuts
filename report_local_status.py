
from DeepWhiskerCuts.setting.setting import common_cache,this_computer,computers
from DeepWhiskerCuts.lib.StatusMonitor import StatusMonitor
from DeepWhiskerCuts.lib.remote_utility import run_python_script
import pdb
monitor = StatusMonitor()
for computer in computers:
    pdb.set_trace()
    run_python_script(computer,'find_status.py')