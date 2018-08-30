import base64
import os


class Encode_Image:

    def encode_image(self, image_Name):
        dir_path = os.path.dirname(os.path.realpath(__file__+"/../../"))
        print(dir_path)
        with open(dir_path+"/static/images/retrieved_images/"+image_Name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        base64_string = encoded_string.decode("utf-8")
        return base64_string
