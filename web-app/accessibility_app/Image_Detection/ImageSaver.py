import urllib.request as urllib
import os
from .Encode_Image import Encode_Image

class ImageSave:

    def save_Image_from_url(self, url, name):
        dir_path = os.path.dirname(os.path.realpath(__file__+"/../../"))
        urllib.urlretrieve(
            url, dir_path+"/static/images/retrieved_images/"+name)
    
    @staticmethod 
    def save_Image_from_url_get_encoded_content(url, name):
        dir_path = os.path.dirname(os.path.realpath(__file__+"/../../"))
        urllib.urlretrieve(
            url, dir_path+"/static/images/retrieved_images/"+name)
        encoded_string=Encode_Image.encode_image(name)
        #os.remove(dir_path+"/static/images/retrieved_images/"+name)
        return encoded_string

