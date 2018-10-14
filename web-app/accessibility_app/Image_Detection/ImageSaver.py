import urllib.request as urllib
import os

class ImageSave:

    def save_Image_from_url(self, url, name):
        dir_path = os.path.dirname(os.path.realpath(__file__+"/../../"))
        urllib.urlretrieve(
            url, dir_path+"/static/images/retrieved_images/"+name)
            
