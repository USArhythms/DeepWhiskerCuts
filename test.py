from MovieTools import make_movie_and_stimulus_file,save_trial_n,extract_eye_videos
import re
import deeplabcut
import os
import shutil
from glob import glob

priority =[ #'/net/dk-server/afassihizakeri/movies_Rat_SC_project/ar19muscimol500ug500nlrightside/10_10_19/',
 '/net/dk-server/afassihizakeri/movies_Rat_SC_project/ar2muscimol500nl500igmlrightside/10_11_19/',
 '/net/dk-server/afassihizakeri/movies_Rat_SC_project/ar19Muscimolrightside500mg500nl/10_19_19/',
 '/net/dk-server/afassihizakeri/movies_Rat_SC_project/ar19Muscimolrightside500mg500nl/10_21_19/',]
for data_path in priority:
    make_movie_and_stimulus_file(data_path,parallel=True,ncores = 16)