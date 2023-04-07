import os
import pandas as pd
import math
from PIL import Image ,ImageEnhance
import numpy as np
import cv2 
import DeepWhiskerCuts.lib.image_util as image_util
import time
import pdb
from DeepWhiskerCuts.setting.dlc_setting import top_view_config_name

def savemovies_LR(movie_name,head_angle,df,good_frames,extension,factor): 
    text = os.path.basename(movie_name);
    video_name = (os.path.join(os.path.dirname(movie_name),text.split('DLC')[0]+extension));
    video_nameR = (os.path.join(os.path.dirname(movie_name),"Mirror"+text.split('DLC')[0]+"R.avi"));
    video_nameL = (os.path.join(os.path.dirname(movie_name),"Mask"+text.split('DLC')[0]+"L.avi"));
    video_name=video_name.split('video.mp4')[0]+'.avi';
    print(video_name)
    process_and_split_video(video_name,video_nameR,good_frames,head_angle,df,factor,315,630,faceshift=60,flip=True)
    process_and_split_video(video_name,video_nameL,good_frames,head_angle,df,factor,0,315,faceshift=80)

def process_and_split_video(input_name,output_name,good_frames,head_angle,df,factor,start_index,end_index,faceshift=60,flip=False):
    cap = cv2.VideoCapture(input_name)
    i=0
    video = cv2.VideoWriter(output_name, 0, 40, (315,700))
    while(cap.isOpened()):
     ret, frame = cap.read() 
     if ret == True:
        i+=1
        if good_frames[i-1]==1:
            color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(color_coverted)
            rotated = image.rotate((math.degrees(head_angle[i-1])-90+180), expand=True)
            rotated = np.array(rotated) 
            rotated = rotated[:, :, ::-1].copy() 
            cropped=  crop_rotated(rotated,frame,head_angle,i-1,df)
            cropped_image = cropped[0:700, start_index+faceshift:end_index+faceshift]
            if flip:
                frame2 = cv2.flip(cropped_image, 1)
            else:
                frame2 = cropped_image
            frame2 = image_util.mask(frame2,60)
            frame2 = Image.fromarray(frame2)
            frame2 = frame2.convert("RGB")
            enhancer = ImageEnhance.Contrast(frame2)
            enhanced = enhancer.enhance(factor)
            video.write(np.array(enhanced))
     else:
        break
    video.release()


def readDLCfiles(data_path,Tag,trial):   
    Xfiles = [os.path.join(data_path,i) for i in os.listdir(data_path) if 'filtered.csv' in i and 'Topview' in i and int(i.split('DLC')[0])==trial]
    try:
        filename = Xfiles[0]
        df = pd.read_csv(filename, header=2 ,usecols=['x','y','likelihood','x.1','y.1','likelihood.1'])
        df.columns=  ['Nosex','Nosey','Noselikelihood','Snoutx1','Snouty1','Snoutlikelihood']
        smoothingwin = 5;
        x1 = smooth_data_convolve_my_average(df.Nosex, smoothingwin);
        y1 = smooth_data_convolve_my_average(df.Nosey, smoothingwin);
        x2 = smooth_data_convolve_my_average(df.Snoutx1, smoothingwin);
        y2 = smooth_data_convolve_my_average(df.Snouty1, smoothingwin);
        head_angles = [math.atan2(-(y1[i]-y2[i]),-(x1[i]-x2[i]))  for i in range(len(df.Snoutlikelihood))] # define the angle of the head
        inter_bead_distance = [math.sqrt((x2[i] - x1[i])**2 + (y2[i] - y1[i])**2)  for i in range(len(df.Snoutlikelihood))]# define the distance between beads  
        head_angles = pd.Series(head_angles)
        return df,head_angles,inter_bead_distance,filename
    except:
        pdb.set_trace()

def find_good_frames(Minliklihood,mindist,maxdist,df,Distance):
    Good_Frames = [0 if df.Noselikelihood[i] <Minliklihood or df.Snoutlikelihood[i] <Minliklihood or Distance[i]<mindist or Distance[i]>maxdist else 1 for i in range(len(df.Snoutlikelihood))]
    a=pd.Series(Good_Frames)
    a[a==0] = np.nan
    return a

def crop_rotated(rotated,frame,Angle,i,df):
    img = Image.fromarray(rotated, 'RGB')
    Newrotated=np.uint8(add_margin(img, 400, 400, 400, 400, (0,0,0)))
    Alpharad = math.radians(math.degrees(Angle[i])-90+180);
    P = [df.Nosey[i] ,df.Nosex[i]]
    c, s = np.cos(Alpharad),np.sin(Alpharad)
    RotMatrix = np.array(((c, -s), (s, c)))
    ImCenterA = np.array(frame.shape[0:2])/2       # Center of the main image
    ImCenterB = np.array(Newrotated.shape[0:2])/2  # Center of the transformed image
    RotatedP =RotMatrix.dot(P-ImCenterA)+ImCenterB;
    midpoint= 350;
    sizetotal = 700;
    ratsiosize = 1.1;
    y= int(RotatedP[0]-midpoint);
    x= int(RotatedP[1]-midpoint*ratsiosize);
    h = sizetotal
    w = int(sizetotal*ratsiosize)
    crop_img = Newrotated[y:y+h, x:x+w]
    return crop_img

def smooth_data_convolve_my_average(arr, span):
    re = np.convolve(arr, np.ones(span * 2 + 1) / (span * 2 + 1), mode="same")
    re[0] = np.average(arr[:span])
    for i in range(1, span + 1):
        re[i] = np.average(arr[:i + span])
        re[-i] = np.average(arr[-i - span:])
    return re

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def writeFrameData(data_path,text,Good_Frames,df,Angle):
    frame_data_path = os.path.join(data_path,text.split('DLC')[0]+'FrameData.xlsx');
    good_frame_id = np.where(np.array(Good_Frames) == 1)[0]
    results=pd.DataFrame({"goodframes":good_frame_id, "Angle":Angle[Good_Frames==1], "Nosex":df.Nosex[Good_Frames==1],"Nosey":df.Nosey[Good_Frames==1],"Snoutx":df.Snoutx1[Good_Frames==1],"Snouty":df.Snouty1[Good_Frames==1]})                     
    writer = pd.ExcelWriter(frame_data_path, engine='xlsxwriter')
    results.to_excel(writer, 'Sheet1')
    writer.save()    

def split_left_and_right_from_top_video(data_path):
    contrastfactor=1.05
    text_files = [os.path.join(data_path,f) for f in os.listdir(data_path) if f.endswith('.mp4') and not f.endswith('L.avi') and not f.endswith('R.avi') and not f.endswith('videopoints.avi') and not f.endswith('videopoints.avi')]
    print(len(text_files))
    for trial in range(len(text_files)):
        t =time.time()
        df, head_angle,interbead_distance,movie_name=readDLCfiles(data_path,top_view_config_name,trial)
        text = os.path.basename(movie_name);
        good_frames =find_good_frames(0.7,5,200,df,interbead_distance)
        writeFrameData(data_path,text,good_frames,df,head_angle)
        savemovies_LR(movie_name,head_angle,df,good_frames,".mp4",contrastfactor) 
        elapsed = time.time() - t 
        video_name = (os.path.join(os.path.dirname(movie_name),text.split('DLC')[0]+".avi"));
        print('Trial=',video_name,'Elapsed',elapsed)
        