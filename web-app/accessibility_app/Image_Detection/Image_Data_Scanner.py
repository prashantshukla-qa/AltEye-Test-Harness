from . import Google_api_request
from . import Encode_Image


class Image_Scanner:

    def __init__(self, match_threshhold):
        self.match_threshhold = match_threshhold
        self.req = Google_api_request.Google_API_Request()

    def Scan_Image(self, url, upload=False):
        result_set = []
        if upload is True:
            en = Encode_Image.Encode_Image()
            content = en.encode_image(url)
            data_dict = self.req\
                .get_Image_Information_from_vision_api_by_upload_file(content)
        else:
            data_dict = self.req.get_Image_Information_from_vision_api(url)
        for data_list in data_dict["responses"][0]["labelAnnotations"]:
            if data_list['score']*100 > self.match_threshhold:
                result_set.append(
                    {'Entity': data_list['description'],
                     'confidence': round(data_list['score']*100, 2)})

        return result_set
