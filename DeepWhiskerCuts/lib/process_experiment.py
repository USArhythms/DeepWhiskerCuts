
from lib.pipeline import processs_side_view_data
from setting.setting import this_computer
import os
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str,help="animal folder to annalyze")
    parser.add_argument("--trial", type=str,help="trial folder to annalyze")
    args = parser.parse_args()
    data_path = os.path.join(this_computer['data_path'],args.folder,args.trial)
    processs_side_view_data(data_path)
