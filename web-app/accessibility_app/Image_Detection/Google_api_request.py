import requests
import json
import os
from .ImageSaver import ImageSave


class Google_API_Request:
    key = "AIzaSyD0NDVKg2A9nwgRCg2KpLLK-eyDKCMQbBc"
    url = "https://vision.googleapis.com/v1/images:annotate"

    def get_Image_Information_from_vision_api(self, Image_url):
        encoded_body = json.dumps({
            "requests": [
                {
                    "image": {
                        "source": {
                            "imageUri":
                            Image_url
                        }
                    },
                    "features": [
                        {
                            "type": "LABEL_DETECTION"

                        },
                        {
                            "type": "TEXT_DETECTION"
                        },
                        # {
                        #     "type": "DOCUMENT_TEXT_DETECTION"
                        # },
                        # {
                        #     "type": "IMAGE_PROPERTIES"
                        # },
                        {
                            "type": "WEB_DETECTION"
                        }

                    ]

                }
            ]
        }) 

        r = requests.post(Google_API_Request.url+'?key=' +
                          Google_API_Request.key,
                          data=encoded_body)
        json_data = json.loads(r.text)
        if 'error' in json_data['responses'][0]:
            if json_data['responses'][0]['error']['code'] == 14 or json_data['responses'][0]['error']['code'] == 3:
                encoded_Image=ImageSave.save_Image_from_url_get_encoded_content(Image_url,os.path.basename(Image_url))
                json_data=self.get_Image_Information_from_vision_api_by_upload_file(encoded_Image)
        return json_data

    def get_Image_Information_from_vision_api_by_upload_file(self,
                                                             Image_content):
        encoded_body = json.dumps({
            "requests": [
                {
                    "image": {
                        "content": Image_content
                    },
                    "features": [
                        {
                            "type": "LABEL_DETECTION"

                        },
                        {
                            "type": "TEXT_DETECTION"
                        },
                         {
                            "type": "WEB_DETECTION"
                        }
                    ]

                }
            ]
        })

        r = requests.post(Google_API_Request.url+'?key=' +
                          Google_API_Request.key,
                          data=encoded_body)
        json_data = json.loads(r.text)
        return json_data
