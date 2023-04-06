from pipeline import *
from DeepWhiskerCuts.lib.top_view_spliter import split_left_and_right_from_top_video

data_path = r'F:\videos\ar37motor\2023_02_22_ 163923'

analyze_top_view_video(data_path)
split_left_and_right_from_top_video(data_path)
analyze_left_video(data_path)
analyze_right_video(data_path)
