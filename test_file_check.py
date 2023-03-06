import os
dir = r'D:\Sidevideos\ar37motor\2023_02_22_ 163949'
files = os.listdir(dir)

dlcs = [i for i in files if 'DLC_' in i]


expected = re.compile(r'session \d+: running')

In [221]: x=re.match(expected, strs)

class DLCList():
    def __init__(self,dlc_list):
        self.dlc_list = dlc_list
        self.dlcs = [DLC(i) for i in self.dlc_list]

class DLC:
    def __init__(self,name):
        self.name = name
        self.trial_number = int(self.name.split('EYEDLC_')[0])

list = DLCList(dlcs)

print('')