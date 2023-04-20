from DeepWhiskerCuts.lib.StatusMonitor import get_current_pc_status
from DeepWhiskerCuts.setting.setting import common_cache,this_computer
import pickle
import os
import pdb

status = get_current_pc_status()
pdb.set_trace()
pickle.dump(status,open(os.path.join(common_cache,f'{this_computer["tag"]}.status'),'wb'))