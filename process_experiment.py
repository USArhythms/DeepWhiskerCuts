
from pipeline import processs_side_view_data
from setting import data_root
import os
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str,
                    help="data path to annalyze")
    args = parser.parse_args()
    data_path = os.path.join(data_root,args.path)
    processs_side_view_data(data_path)
