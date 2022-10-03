def makemovieandLightfile(mainfolder):
    # this function is to create movies out of images taken from the camera
    # another fucntion of this script is to extract Mock LEDs locataion (marked by the user Left, center, right)
    
    import xlsxwriter  # this is to write xls files 
    import os # this is to get folder information and creat files 
    import cv2 # this is important and is reading and writing images and video 
    import shutil # to remove folder and subfolders
    import image_util
    my_file = os.path.join(mainfolder+'\Lighttime.xlsx');
    workbook = xlsxwriter.Workbook(my_file)
    worksheet = workbook.add_worksheet()

    col = 0
    All_Folders=[ name for name in os.listdir(mainfolder) if os.path.isdir(os.path.join(mainfolder, name)) ]
    #All_Folders = All_Folders[1];
    #print(All_Folders)
    for num in range(0,len(All_Folders)): 
     KK = os.path.join(mainfolder+os.sep, All_Folders[num])
     KKavi =  os.path.join(mainfolder+os.sep, All_Folders[num]+'.avi')
     #if os.path.isfile(KKavi):
      # continue
     if not os.path.isdir(KK):
      continue
     dirContents = os.listdir(KK)
     if len(dirContents) == 0:
      shutil.rmtree(KK, ignore_errors=False, onerror=None)
      continue
     col +=1
     os.chdir(KK)
     print(num)
     images=image_util.get_image_names(All_Folders,num,KK)
     #print(images[0])   
     if num < 1:
      frame = cv2.imread(os.path.join(mainfolder, images[0]))
      (xL,yL,wL,hL) = cv2.selectROI('image', frame)
      (xC,yC,wC,hC) = cv2.selectROI('image', frame)
      (xR,yR,wR,hR) = cv2.selectROI('image', frame)
     video_name = (KK + '.avi');
     video_name2 =(KK+'video'+ '.mp4');
     worksheet=image_util.make_movies_out_of_images(images, video_name, mainfolder, worksheet,xL,yL,wL,hL,xC,yC,wC,hC,xR,yR,wR,hR,col)
     image_util.convert_video(video_name, video_name2)
    workbook.close()
    return worksheet