def RunMask(Mainfolder):
    from PIL import Image
    import numpy as np
    import cv2 # this is important and is reading and writing images and video
    import image_util
    import os
    from pathlib import Path

    XfilesR = [os.path.join(Mainfolder,f) for f in os.listdir(Mainfolder) if f.endswith('R.avi') and not f.startswith('Mirror')] # find all       files with R.avi as file name
    Xfiles2 = [Path(f) for f in XfilesR] # make each file name path to extract the parents and anme
    XfilesR3 = [os.path.join(f.parents[0],'Mirror'+f.name) for f in Xfiles2] # creat a same as files but with Mirror added to the file names
    Mainfolders =  [os.path.join(f.parents[0],f.stem[:-1]) for f in Xfiles2]
    XfilesL = [os.path.join(Mainfolder,f) for f in os.listdir(Mainfolder) if f.endswith('L.avi') and not f.startswith('Mask')] # find all 
    Xfiles2 = [Path(f) for f in XfilesL] # make each file name path to extract the parents and anme
    XfilesL3 = [os.path.join(f.parents[0],'Mask'+f.name) for f in Xfiles2] # creat a same as files but with Mirror added to the file names
    for thisindex,moviesind in enumerate(XfilesR):
        enhancer=1.1
        video_name = XfilesR[thisindex];
        cap = cv2.VideoCapture(video_name)# reading the videofile
        frame_width  = np.uint8(cap.get(3)) # float
        frame_height = np.uint8(cap.get(4)) # float
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        ret, frame = cap.read()
        height, width, layers = frame.shape

        out = cv2.VideoWriter(XfilesR3[thisindex],fourcc, 1,( height, width))
        i = 0
        while(cap.isOpened()):
         # Capture frame-by-frame
         ret, frame = cap.read()
         #print(ret)
         if ret == True:
          frame2 = cv2.flip(frame, 1)
          frame2 = image_util.mask(frame2,60)
          frame2 =frame2*enhancer
          cv2.imwrite(os.path.join(Mainfolders[thisindex],'R_mirror'+str(i)+'.jpg'),frame2)
          i+=1
         else:
          break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        import os
        Mainfolder = Mainfolders[thisindex]
        files = [os.path.join(Mainfolder,f)  for f in os.listdir(Mainfolder) if f.startswith('R_mirror')] # add path to each file
        frame = cv2.imread(os.path.join(Mainfolder, files[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(XfilesR3[thisindex], 0, 40, (width,height))
        fps = 40
        files.sort(key=lambda x: os.path.getmtime(x))
        images = files
        for idx,image in enumerate(images):
        #worksheet.write_row( idx+1,col, mat)
            frame = cv2.imread(os.path.join(Mainfolder, images[idx]))
            video.write(frame)
        cv2.destroyAllWindows()
        video.release()
        [os.remove(os.path.join(Mainfolder,f)) for f in  images]

    #Xfiles4= Xfiles4[156:];

    for thisindex,moviesind in enumerate(XfilesL):
        enhancer=1.1
        video_name = XfilesL[thisindex];
        cap = cv2.VideoCapture(video_name)# reading the videofile
        frame_width  = np.uint8(cap.get(3)) # float
        frame_height = np.uint8(cap.get(4)) # float
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        ret, frame = cap.read()
        height, width, layers = frame.shape

        out = cv2.VideoWriter(XfilesL3[thisindex],fourcc, 1,( height, width))
        i = 0
        while(cap.isOpened()):
         # Capture frame-by-frame
         ret, frame = cap.read()
         print(ret)
         if ret == True:
          frame2 =frame
          frame2 = image_util.mask(frame2,60)
          frame2 =frame2*enhancer

          cv2.imwrite(os.path.join(Mainfolders[thisindex],'Mask'+str(i)+'.jpg'),frame2)
          i+=1
         else:
          break


        cap.release()
        out.release()
        cv2.destroyAllWindows()
        import os
        Mainfolder = Mainfolders[thisindex]
        files = [os.path.join(Mainfolder,f)  for f in os.listdir(Mainfolder) if f.startswith('Mask')] # add path to each file
        frame = cv2.imread(os.path.join(Mainfolder, files[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(XfilesL3[thisindex], 0, 40, (width,height))
        fps = 40
        files.sort(key=lambda x: os.path.getmtime(x))
        images = files
        for idx,image in enumerate(images):
        #worksheet.write_row( idx+1,col, mat)
            frame = cv2.imread(os.path.join(Mainfolder, images[idx]))
            video.write(frame)
        cv2.destroyAllWindows()
        video.release()
        [os.remove(os.path.join(Mainfolder,f)) for f in  images]

