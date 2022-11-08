
from pipeline import processs_side_view_data
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    data_path = r'D:\Sidevideos\ar37motor\2022_07_28'
    parser.add_argument("path", type=str,
                    help="data path to annalyze")
    args = parser.parse_args()
    data_path = args.path
    processs_side_view_data(data_path)
