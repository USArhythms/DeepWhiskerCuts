import os 
import image_util

class MovieMaker:
    def make_movie(self,folderi,*args):
        images=image_util.get_image_names(self.dir)
        temp_video_path = os.path.join('/media/zhw272/Samsung_T5/videos','/'.join(self.dir.split('/')[-4:]))
        avi_name = (temp_video_path + '.avi')
        mp4_name =(temp_video_path+'video'+ '.mp4')
        image_util.make_movies(images, avi_name)
        image_util.convert_video(avi_name, mp4_name)
        return folderi