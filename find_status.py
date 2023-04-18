from DeepWhiskerCuts.lib.StatusMonitor import get_current_pc_status
from DeepWhiskerCuts.setting.setting import common_cache,this_computer
import pickle
import os
status = get_current_pc_status()
pickle.dumps(status,open(os.path.join(common_cache,f'{this_computer["tag"]}.status'),'wb'))