from . import Google_api_request
from . import Encode_Image
from . import ImageSaver
import  re


class Image_Scanner:

    def __init__(self, match_threshhold):
        self.match_threshhold = match_threshhold
        self.req = Google_api_request.Google_API_Request()
        self.data_dict = None
        self.text_from_Image = []

    def Scan_Image(self, url, upload=False):

        self.is_text_present_in_Image = None
        result_set = []
        islocal="local://" in url
        if upload is True or islocal:
            print("using upload")
            filename=re.search("local://(.+)$",url).group(1)
            en = Encode_Image.Encode_Image()
            content = en.encode_image(filename)
            self.data_dict = self.req\
                .get_Image_Information_from_vision_api_by_upload_file(content)
        else:
            self.data_dict = self.req.get_Image_Information_from_vision_api(
                url)
        try:
            print("Here...1")
            for data_list in self.data_dict["responses"][0]["labelAnnotations"]:
                if data_list['description'] in "text":
                    self.is_text_present_in_Image = True
                if data_list['score']*100 > self.match_threshhold:
                    result_set.append(
                        {'Entity': data_list['description'],
                         'confidence': round(data_list['score']*100, 2)})

                for data_list in self.data_dict["responses"][0]["webDetection"]["webEntities"]:
                    if 'description' in data_list:
                        result_set.append(
                            {'Entity': data_list['description']+" (Web-Entity)",
                             'confidence': round(data_list['score'], 2)})

                if self.is_text_present_in_Image:
                    text = self.data_dict["responses"][0]["fullTextAnnotation"]['text']
                    text_from_Image_list = text.split("\n")
                    for eachtext in text_from_Image_list:
                        if eachtext=="":
                            continue
                        self.text_from_Image.append({'Entity': eachtext,
                                                     'confidence': self.match_threshhold})
        except KeyError as error:
            print(error)
            if "labelAnnotations" in str(error):
                
                return [{'Entity': "None:Error Occured", 'confidence': 0, }]
            else:
                return result_set
        for each_data in result_set:
            if each_data['Entity']=="":
                result_set.remove(each_data)
        return result_set

    def get_Text_list_From_Image(self):
        return self.text_from_Image

    def is_Text_Present_In_Image(self):
        return self.is_text_present_in_Image
