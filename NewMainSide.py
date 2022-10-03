def makemovieandLightfile(mainfolder):
    import xlsxwriter  # this is to write xls files 
    import os # this is to get folder information and creat files 
    import cv2 # this is important and is reading and writing images and video 
    import shutil # to remove folder and subfolders
    import image_util
    import PIL
    import numpy
    from PIL import Image
    All_Folders=[ name for name in os.listdir(mainfolder) if os.path.isdir(os.path.join(mainfolder, name)) ]
    # Access all PNG files in directory
    for num in range(0,len(All_Folders)): 
        KK = os.path.join(mainfolder+os.sep, All_Folders[num])
        
        # =os.listdir(KK)
        thisim = (os.path.join(mainfolder+os.sep, All_Folders[num],'50.jpeg'))

        # Create a numpy array of floats to store the average (assume RGB images)
        if  num < 1:  
            w,h=Image.open(thisim).size
            arr=numpy.zeros((h,w,3),numpy.float)
            imlist= [thisim]  
        imlist.append(thisim) 

        # Build up average pixel intensities, casting each image as an array of floats
    N=len(imlist)
    arr=numpy.zeros((h,w),numpy.float)
    for im in imlist:
        imarr=numpy.array(Image.open(im),dtype=numpy.float)
        arr=arr+imarr/N

    # Round values in array and cast as 8-bit integer
    arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)
    
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
      # frame = cv2.imread(os.path.join(mainfolder, images[0]))
      (xL,yL,wL,hL) = cv2.selectROI('image', arr)
      (xC,yC,wC,hC) = cv2.selectROI('image', arr)
      (xR,yR,wR,hR) = cv2.selectROI('image', arr)
     video_name = (KK + '.avi');
     video_name2 =(KK+'video'+ '.mp4');
     worksheet=image_util.make_movies_out_of_images(images, video_name, mainfolder, worksheet,xL,yL,wL,hL,xC,yC,wC,hC,xR,yR,wR,hR,col)
     image_util.convert_video(video_name, video_name2)
    workbook.close()
    return worksheet

def make_movie_only(mainfolder):
    import os # this is to get folder information and creat files 
    import cv2 # this is important and is reading and writing images and video 
    import shutil # to remove folder and subfolders
    import image_util
    import PIL
    import numpy
    from PIL import Image
    


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
         #print(images[0])   
         images=image_util.get_image_names(All_Folders,num,KK)
         
         video_name = (KK + '.avi');
         video_name2 =(KK+'video'+ '.mp4');
         image_util.make_movies_out_of_imagesNocropp(images, video_name, mainfolder)
         image_util.convert_video(video_name, video_name2)

def save_trial_n(mainfolder):

    import os # this is to get folder information and creat files 
    import cv2 # this is important and is reading and writing images and video 
    import shutil # to remove folder and subfolders
  

    col = 0
    All_Folders=[ name for name in os.listdir(mainfolder) if os.path.isdir(os.path.join(mainfolder, name)) ]
    #All_Folders = All_Folders[1];
    print(All_Folders)
    #
    with open(os.path.join(mainfolder, 'Trialnfrompython.txt'), 'w') as f:
       for item in All_Folders:
          f.write("%s\n" % item)
        
    f.close()   
    
   

def make_movie_and_stimulus_file(mainfolder):
    import xlsxwriter  # this is to write xls files 
    import os # this is to get folder information and creat files 
    import cv2 # this is important and is reading and writing images and video 
    import shutil # to remove folder and subfolders
    import image_util
    my_file = os.path.join(mainfolder+'\Lighttimeremainings.xlsx');
    workbook = xlsxwriter.Workbook(my_file)
    worksheet = workbook.add_worksheet()

    col = 0
    All_Folders=[ name for name in os.listdir(mainfolder) if os.path.isdir(os.path.join(mainfolder, name)) ]
    #All_Folders = All_Folders[1];
    #print(All_Folders)
    for num in range(0,len(All_Folders)): 
     KK = os.path.join(mainfolder+os.sep, All_Folders[num])
     KKavi =  os.path.join(mainfolder+os.sep, All_Folders[num]+'.avi')
     if os.path.isfile(KKavi):
       continue
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
     if col < 1:
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


   


