import os
import argparse
from setting import this_computer

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str,
                    help="animal folder")
    args = parser.parse_args()
    print(os.listdir(os.path.join(this_computer['data_path'],args.folder)))
