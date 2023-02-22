
import os
from pipeline import processs_side_view_data
from MovieTools import make_movie_and_stimulus_file
dir = r'D:\Sidevideos\ar44motor\2023_02_17_ 134703'
make_movie_and_stimulus_file(dir,parallel=False,ncores = 6)
