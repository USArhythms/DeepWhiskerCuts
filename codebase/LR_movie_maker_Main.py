def savemovies_LR(movivename,Angle,df,Good_Frames,Extention,factor): 
    from PIL import Image ,ImageEnhance
    from scipy import ndimage
    import numpy as np
    import cv2 # this is important and is reading and writing images and video
    import image_util
    import os
    from pathlib import Path
    import datetime
    import math
    import image_util
    
    text = os.path.basename(movivename);
    video_name = (os.path.join(os.path.dirname(movivename),text.split('DLC')[0]+Extention));
    video_nameR = (os.path.join(os.path.dirname(movivename),"Mirror"+text.split('DLC')[0]+"R.avi"));
    video_nameL = (os.path.join(os.path.dirname(movivename),"Mask"+text.split('DLC')[0]+"L.avi"));
    video_name=video_name.split('video.mp4')[0]+'.avi';
    print(video_name)
    cap = cv2.VideoCapture(video_name)# reading the videofile
    frame_width  = np.uint8(cap.get(3)) # float
    frame_height = np.uint8(cap.get(4)) # float
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    i=0
    #factor=1.5;
    video = cv2.VideoWriter(video_nameR, 0, 40, (315,700))

    faceshift=60;
    while(cap.isOpened()):
     ret, frame = cap.read() 
     if ret == True:
        i+=1
        height, width, layers = frame.shape
        #rotation angle in degree
        if Good_Frames[i-1]==1:
            #rotated = ndimage.rotate(frame, math.degrees(Angle[i-1])-90+180)
            color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(color_coverted)
            out = pil_image.rotate((math.degrees(Angle[i-1])-90+180), expand=True)
            open_cv_image = np.array(out) 
            rotated = open_cv_image[:, :, ::-1].copy()   # Convert RGB to BGR 
            cropped=  crop_rotated(rotated,frame,Angle,i-1,df)
            sub_imageR = cropped[0:700, 315+faceshift:630+faceshift]
            frame2 = cv2.flip(sub_imageR, 1)
            frame2 = image_util.mask(frame2,60)
            frame2 = Image.fromarray(frame2)
            frame2 = frame2.convert("RGB")
            enhancer = ImageEnhance.Contrast(frame2)
            im_output = enhancer.enhance(factor)
            #cv2.imshow("video", np.array(im_output))
            #cv2.waitKey(1)
            video.write(np.array(im_output))

        #Mirror92R

     else:
        break
    video.release()



    cap = cv2.VideoCapture(video_name)# reading the videofile
    frame_width  = np.uint8(cap.get(3)) # float
    frame_height = np.uint8(cap.get(4)) # float
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    i=0
    factor=1.5;
    video = cv2.VideoWriter(video_nameL, 0, 40, (315,700))

    faceshift=80
    while(cap.isOpened()):
     ret, frame = cap.read() 
     if ret == True:
        i+=1
        height, width, layers = frame.shape
        #rotation angle in degree
        if Good_Frames[i-1]==1:
            color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(color_coverted)
            out = pil_image.rotate((math.degrees(Angle[i-1])-90+180), expand=True)
            open_cv_image = np.array(out) 
            rotated = open_cv_image[:, :, ::-1].copy()   # Convert RGB to BGR 
            cropped=  crop_rotated(rotated,frame,Angle,i-1,df)
            sub_imageL = cropped[0:700, 0+faceshift:315+faceshift]
            frame2 = image_util.mask(sub_imageL,60)
            frame2 = Image.fromarray(frame2)
            frame2 = frame2.convert("RGB")
            enhancer = ImageEnhance.Contrast(frame2)
            im_output = enhancer.enhance(factor)
            #cv2.imshow("video", np.array(im_output))
            #cv2.waitKey(1)
            video.write(np.array(im_output))

        #Mirror92R

     else:
        break
    video.release()


# this function read dlc 
def readDLCfiles(Mainfolder,Tag,trial):
    #11185DLC_resnet50_Topview3435Jul28shuffle1_110000_filtered
    import csv
    import os
    import pandas as pd
    from scipy.spatial.distance import pdist
    import math
    import matplotlib.pyplot as plt
   
    Xfiles = [os.path.join(Mainfolder,f) for f in os.listdir(Mainfolder) if f.endswith('filtered.csv') and Tag in f] 
    # csv file name
    filename = Xfiles[trial] # select the trial
    df = pd.read_csv(filename, header=2 ,usecols=['x','y','likelihood','x.1','y.1','likelihood.1'])
    df.columns=  ['Nosex','Nosey','Noselikelihood','Snoutx1','Snouty1','Snoutlikelihood']
 
    # smooth the xy coordinates by simple avaraging 
    smoothingwin = 5;
    x1 = smooth_data_convolve_my_average(df.Nosex, smoothingwin);
    y1 = smooth_data_convolve_my_average(df.Nosey, smoothingwin);
    x2 = smooth_data_convolve_my_average(df.Snoutx1, smoothingwin);
    y2 = smooth_data_convolve_my_average(df.Snouty1, smoothingwin);


    Angles = [math.atan2(-(y1[i]-y2[i]),-(x1[i]-x2[i]))  for i in range(len(df.Snoutlikelihood))] # define the angle of the head
    Distance = [math.sqrt((x2[i] - x1[i])**2 + (y2[i] - y1[i])**2)  for i in range(len(df.Snoutlikelihood))]# define the distance between beads  
    Angles=pd.Series(Angles)
    #Angles[Angles<-2]= Angles[Angles<-2]+2*math.pi;
    return df,Angles,Distance,filename
# measure goodfrmaes
def find_good_frames (Minliklihood,mindist,maxdist,df,Distance):
    Good_Frames = [0 if df.Noselikelihood[i] <Minliklihood or df.Snoutlikelihood[i] <Minliklihood or Distance[i]<mindist or Distance[i]>maxdist else 1 for i in range(len(df.Snoutlikelihood))]
    import pandas as pd
    import numpy as np
    a=pd.Series(Good_Frames)
    a[a==0] = np.nan
    return a
# crop the image centered on nose and new rotation matrix based on angle 

def crop_rotated(rotated,frame,Angle,i,df):
    from PIL import Image
    import numpy as np
    import math
    img = Image.fromarray(rotated, 'RGB')
    Newrotated=np.uint8(add_margin(img, 400, 400, 400, 400, (0,0,0)))
    Alpha = math.degrees(Angle[i])-90+180;
    Alpharad = math.radians(math.degrees(Angle[i])-90+180);
    utP = [df.Nosex[i] ,df.Nosey[i]]
    P = [df.Nosey[i] ,df.Nosex[i]]
    #P = [thiscenter[2],thiscenter[1]]   #coordinates of point
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

 #yourImage2 = imcrop(RotatedIm,[RotatedP(2)-midpoint RotatedP(1)-midpoint*0.6 sizetotal sizetotal*ratsiosize]);

def smooth_data_convolve_my_average(arr, span):
    import numpy as np
    re = np.convolve(arr, np.ones(span * 2 + 1) / (span * 2 + 1), mode="same")
        # The "my_average" part: shrinks the averaging window on the side that 
    # reaches beyond the data, keeps the other side the same size as given 
    # by "span"
    re[0] = np.average(arr[:span])
    for i in range(1, span + 1):
        re[i] = np.average(arr[:i + span])
        re[-i] = np.average(arr[-i - span:])
    return re

# this function adds margin to the image (this is done to have the cropped size equal in all images)
def add_margin(pil_img, top, right, bottom, left, color):
    from PIL import Image
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result
def writeFrameData(Mainfolder,text,Good_Frames,df,Angle):
    import os
    from tabulate import tabulate
    import pandas as pd
    import xlsxwriter  # this is to write xls files 
    import numpy as np
    my_file = os.path.join(Mainfolder,text.split('DLC')[0]+'FrameData.xlsx');
    pos = np.where(np.array(Good_Frames) == 1)[0]
    results=pd.DataFrame({"goodframes":pos, "Angle":Angle[Good_Frames==1], "Nosex":df.Nosex[Good_Frames==1]\
    ,"Nosey":df.Nosey[Good_Frames==1],"Snoutx":df.Snoutx1[Good_Frames==1],"Snouty":df.Snouty1[Good_Frames==1]})                     

    # Specify a writer
    writer = pd.ExcelWriter(my_file, engine='xlsxwriter')
    yourData=tabulate(results, headers=["goodframes", "Angle", "Nosex","Nosey","Snoutx","Snouty"]);
    # Write your DataFrame to a file   
    results.to_excel(writer, 'Sheet1')
    # Save the result
    writer.save()    
