import xlsxwriter  
import os 
import cv2 
import shutil 
from DeepWhiskerCuts.setting.dlc_setting import side_view_config_name,side_view_shuffle
import DeepWhiskerCuts.lib.image_util as image_util
from PIL import Image
import numpy as np
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor,as_completed
from DeepWhiskerCuts.utility.logger import log_error
import pdb
import re 

def start_video(file_name):
    path,movie_name = os.path.split(file_name)
    movie_name = movie_name.split('DLC')[0]
    video_name = (os.path.join(path,movie_name+'.avi'));
    eye_video_name = (os.path.join(path,movie_name+"EYE.avi"));
    capture = cv2.VideoCapture(video_name)
    video = cv2.VideoWriter(eye_video_name, 0, 40, (200,200))
    return capture,video

def extract_single_eye_video(file_name):
    eye_position = pd.read_csv(file_name, header=2 ,usecols=['x','y','likelihood','x.1','y.1','likelihood.1','x.2','y.2','likelihood.2'])
    eye_position.columns=  ['Nosex','Nosey','Noselikelihood','Snoutx1','Snouty1','Snoutlikelihood','Eyex','Eyey','Eyelikelihood']
    capture,video = start_video(file_name)
    i=0
    while(capture.isOpened()):
        continue_to_read, frame = capture.read()
        if continue_to_read == True:
            i+=1
            color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(color_coverted, 'RGB')
            Newrotated=np.uint8(image_util.add_margin(img, 100, 100, 100, 100, (0,0,0)))
            y= int(eye_position.Eyey[i-1]);
            x= int(eye_position.Eyex[i-1]);
            margin = 200
            crop_img = Newrotated[y:y+margin, x:x+margin]
            video.write(np.array(crop_img))
        else:
            break
    video.release()

def extract_eye_videos(data_path,Tag):
    side_view_dlc = rf'DLC_\w+{side_view_config_name}\w+shuffle{side_view_shuffle}_\d+.csv'
    csv_files = [i for i in os.listdir(data_path) if re.match(side_view_dlc, i.replace(' ', '_'))!=None]
    nfiles = len(csv_files)
    for filei in tqdm(range(nfiles),'extracting eye videos'): 
        file_name = csv_files[filei] 
        try:
            extract_single_eye_video(file_name)
        except BaseException as ex:
            log_error(data_path,'Error during eye video creation for: '+file_name,ex)

def list_all_folders_in_directory(directory):
    return [ name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) ]

def get_width_and_height_of_image(path,all_png_folders):
    path_to_folderi = os.path.join(path,all_png_folders[0])
    if len(os.listdir(path_to_folderi))==0:
        return None,None
    path_to_imagei = os.listdir(path_to_folderi)[0] 
    return Image.open(os.path.join(path,all_png_folders[0],path_to_imagei)).size

def get_average_image(path,all_png_folders):
    image_paths= [] 
    width,height=get_width_and_height_of_image(path,all_png_folders)
    for folderi in range(len(all_png_folders)): 
        path_to_folderi = os.path.join(path,all_png_folders[folderi])
        if os.listdir(path_to_folderi)==[]:
            # os.rmdir(path_to_folderi)
            continue
        path_to_imagei = [i for i in os.listdir(path_to_folderi) if '40.' in i and '.h5' not in i][0]
        image_paths.append(os.path.join(path_to_folderi,path_to_imagei)) 
    n_image=len(image_paths)
    if height==None:
        return
    average_image=np.zeros((height,width),np.float)
    for image_pathi in image_paths:
        try:
            image = Image.open(image_pathi);
        except:
            ...
        average_image+=np.array(image,dtype=np.float)
    average_image=average_image/n_image
    average_image=np.array(np.round(average_image),dtype=np.uint8)
    return average_image

def make_movie(trial_folder,image_names):
    temp_video_path = os.path.join('/media/zhw272/Samsung_T5/videos','/'.join(trial_folder.split('/')[-4:]))
    avi_name = (trial_folder + '.avi')
    mp4_name =(trial_folder+'video'+ '.mp4')
    image_util.make_movies(image_names, avi_name)
    image_util.convert_video(avi_name, mp4_name)

def make_movie_for_all_trials(path,parallel=False,ncores = None):
    all_png_folders=list_all_folders_in_directory(path)
    nfolders = len(all_png_folders)
    trial_folders = []
    image_names = []
    stimulus_value = {}
    for folderi in tqdm(range(nfolders),'processing videos'): 
            trial_folder = all_png_folders[folderi]
            trial_folder = os.path.join(path, trial_folder)
            if not os.path.isdir(trial_folder):
                continue
            names=image_util.get_image_names(trial_folder)
            image_names.append(names)
            trial_folders.append(trial_folder)
    if parallel:
        with ProcessPoolExecutor(max_workers=ncores) as executor:
            results = []
            for folderi in range(nfolders): 
                trial_folder = trial_folders[folderi]
                result= executor.submit(make_movie,trial_folder,image_names[folderi])
            for result in as_completed(results):
                try:
                    result.result()
                except BaseException as ex:
                    log_error(path,'Error during avi creation for: '+trial_folders[folderi],ex)
    else:
        for folderi in tqdm(range(nfolders),'processing videos'): 
            trial_folder = trial_folders[folderi]
            try:
                make_movie(trial_folder,image_names[folderi])
            except BaseException as ex:
                log_error(path,'Error during avi creation for: '+trial_folder,ex)
    return stimulus_value

def get_led_position_from_user_input(average_image):
    left_led_postion = cv2.selectROI('image', average_image)
    center_led_position = cv2.selectROI('image', average_image)
    right_led_position = cv2.selectROI('image', average_image)
    return left_led_postion,center_led_position,right_led_position

def get_place_holder_led_position():
    left_led_postion=[1,2,3,4]
    center_led_position=[1,2,3,4]
    right_led_position=[1,2,3,4]
    return left_led_postion,center_led_position,right_led_position

def extract_stimulus_information(path,parallel=False,ncores = None):
    average_image = get_average_image(path,all_png_folders)
    excel_file = os.path.join(path,'Lighttime.xlsx')
    left_led_postion,center_led_position,right_led_position = get_led_position_from_user_input(average_image)
    create_stimulus_worksheet(excel_file,stimulus_value)

def create_stimulus_worksheet(excel_file,stimulus_value):
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet()
    for folderi in stimulus_value:
        folderi_stimulus_value = stimulus_value[folderi]
        nframe = len(folderi_stimulus_value)
        for framei in range(nframe):
            stimulus_left,stimulus_center,stimulus_right = folderi_stimulus_value[framei]
            worksheet.write_row(framei + 1, folderi, [stimulus_left])
            worksheet.write_row(framei + 501, folderi, [stimulus_center])
            worksheet.write_row(framei + 1001, folderi, [stimulus_right])
    workbook.close()

def save_trial_n(path):
    all_png_folders=list_all_folders_in_directory(path)
    print(all_png_folders)
    with open(os.path.join(path, 'Trialnfrompython.txt'), 'w') as f:
       for item in all_png_folders:
          f.write("%s\n" % item)
    f.close()   

