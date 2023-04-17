import os
import argparse
import pdb
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder')
    args = parser.parse_args()
    folders = os.listdir(args.folder)
    output = '['+','.join(folders)+']'
    print(output)