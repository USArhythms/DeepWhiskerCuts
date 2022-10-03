

def get_image_names(All_Folders,num,KK):
     import os  # this is to get folder information and creat files
     import cv2  # this is important and is reading and writing images and video
     files = filter(os.path.isfile, os.listdir(KK));
     files = [os.path.join(KK, f) for f in files if f] # add path to each file
     files.sort(key=lambda x: os.path.getmtime(x))

     nwefiles = [os.path.splitext(os.path.basename(f)) for f in  files] # add path to each file
     Prefix =  nwefiles[0]
     Prefix = Prefix[0] 
     nwefiles = [(f[0]) for f in nwefiles if f[0].startswith('Mask')]
     nwefiles = [os.path.join(KK, f+'.jpg') for f in  nwefiles] # add path to each file
     [os.remove(f) for f in  nwefiles]
     nwefiles = [os.path.splitext(os.path.basename(f)) for f in  files] # add path to each file
     nwefiles = [(f[0]) for f in nwefiles if f[0].startswith('R_mirror')]
     nwefiles = [os.path.join(KK, f+'.jpg') for f in  nwefiles]
     [os.remove(f) for f in  nwefiles]
     nwefiles = [os.path.splitext(os.path.basename(f)) for f in  files] # add path to each file
     nwefiles = [(f[0]) for f in nwefiles if not f[0].startswith('Mask') and not f[0].startswith('R_mirror')]
     nwefiles = [(int(f[-3:])) for f in nwefiles]
     nwefiles = sorted(nwefiles)
     nwefiles = ["%03d" % x for x in nwefiles]
     files = [os.path.join(KK, Prefix[0:-3] + str(f) + '.jpg') for f in nwefiles]  # add path to each file

     return files


def make_movies_out_of_images(images, video_name, mainfolder, worksheet,xL,yL,wL,hL,xC,yC,wC,hC,xR,yR,wR,hR,col):
    import os  # this is to get folder information and creat files
    import cv2  # this is important and is reading and writing images and video 
    import numpy as np
    frame = cv2.imread(os.path.join(mainfolder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 40, (width, height))
    fps = 40

    for idx, image in enumerate(images):
        # worksheet.write_row( idx+1,col, mat)
        frame = cv2.imread(os.path.join(mainfolder, images[idx]))
        video.write(frame)

        cropped_l = frame[yL:yL + hL, xL:xL + wL]  # both opencv and numpy are "row-major", so y goes first
        cropped_r = frame[yR:yR + hR, xR:xR + wR]  # both opencv and numpy are "row-major", so y goes first
        cropped_c = frame[yC:yC + hC, xC:xC + wC]  # both opencv and numpy are "row-major", so y goes first
        worksheet.write_row(idx + 1, col, [np.mean(cropped_l)])
        worksheet.write_row(idx + 501, col, [np.mean(cropped_c)])
        worksheet.write_row(idx + 1001, col, [np.mean(cropped_r)])
    video.release()
    cv2.destroyAllWindows()
    return worksheet
    
def convert_video(video_input, video_output):
    import subprocess
    cmds = ['ffmpeg', '-i', video_input, video_output]
    subprocess.Popen(cmds)  



def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """

    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)
   
def Mask(frame2,sigma):
    import numpy as np
    [x1,x2,x3]=frame2.shape;
    center = [x1 ,x1/2]
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    g=np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / sigma**2) 
    g=np.delete(g, list(range(x1-x2)), 1)

    y = np.expand_dims(g, axis=3)
    y=np.repeat(y,3,axis=2)
    a = np.array(frame2, dtype=float)
    a = a*(1-y)
    img = a.astype(np.uint8)

    return(img)

   


