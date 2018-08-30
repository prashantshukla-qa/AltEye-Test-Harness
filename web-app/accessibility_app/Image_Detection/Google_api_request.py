import requests
import json


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
