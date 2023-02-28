
from ProgressManager import ExperimentManager
from MovieTools import make_movie_and_stimulus_file


dir = r'D:\Sidevideos\ar37motor\2023_02_17_ 114921'
make_movie_and_stimulus_file(dir,parallel=False,ncores = 6)
manager = ExperimentManager(dir,mode = 'side')
manager.copy_full_resolution_videos(r'\\dk-server.dk.ucsd.edu\afassihizakeri\eyemovies\Leftcam1')

dir = r'D:\Sidevideos\AR44MOTOR\2023_02_17_ 134706'
manager = ExperimentManager(dir,mode = 'side')
manager.copy_full_resolution_videos(r'\\dk-server.dk.ucsd.edu\afassihizakeri\eyemovies\Leftcam1')