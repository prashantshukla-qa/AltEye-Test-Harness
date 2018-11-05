from selenium import webdriver
import urllib.request
import os
SERVER_URL = "http://localhost:5000"
import json
import requests
import urllib

class Image_Chrome_Webdriver(webdriver.Chrome):
    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):

        super().__init__(executable_path, port, options, service_args, desired_capabilities, service_log_path,
                         chrome_options, keep_alive)

    def Test_Alt_Text_Relevancy(self, url, alt, vicinity, method="googleAPI", model="DenseNet", Threshold=30):
        if ".svg" in url:
            print("SVG format is not supported!!")
            return
        url_Complete = SERVER_URL+"/api/get_alt_relevancy/?url="+url+"&alt="+alt + \
            "&vicinity="+vicinity+"&method="+method + \
            "&model="+model+"&Threshold="+str(Threshold)
        url_Complete = url_Complete.replace(" ", "%20")
        Response = requests.get(url_Complete)
        json_acceptable_string = Response.text
        Result = json.loads(json_acceptable_string)
        try:
            possible_texts = [x['Entity'] for x in Result['possible_texts']]
            assert Result['result'] == "GREEN", "Expected the Text classes" + \
                str(Result['text_classes']) + \
                " to be in Image Classes "+str(possible_texts)
            print("\n")
            print("This Image "+url+" has alt text " +
                  alt+" and text is relevant to Image")
        except AssertionError as error:
            print("\n")
            print("This Image "+url+" has alt text "+alt +
                  " and it seems text is not relevant to Image")
            print("Expected the Text classes" +
                  str(Result['text_classes'])+" to be in Image Classes "+str(possible_texts))

    def Test_Alt_Text_Relevancy_via_post(self, path, alt, vicinity, method="googleAPI", model="DenseNet", Threshold=30, custommodel=None, customjson=None):
        if ".svg" in path:
            print("SVG format is not supported!!")
            return
        url_Complete = SERVER_URL+"/api/upload_image_get_relevancy"
        Response = requests.post(url_Complete, files={'file':open(path,'rb')},data={'alt': alt, 'method': method,
                                                     'model': model, 'Threshold': Threshold, 'customjsonfile': customjson, 'custommodel': custommodel})
        json_acceptable_string = Response.text
        Result = json.loads(json_acceptable_string)
        try:
            possible_texts = [x['Entity'] for x in Result['possible_texts']]
            assert Result['result'] == "GREEN", "Expected the Text classes" + \
                str(Result['text_classes']) + \
                " to be in Image Classes "+str(possible_texts)
            print("\n")
            print("This Image in"+path+" has alt text " +
                  alt+" and text is relevant to Image")
        except AssertionError as error:
            print("\n")
            print("This Image "+path+" has alt text "+alt +
                  " and it seems text is not relevant to Image")
            print("Expected the Text classes" +
                  str(Result['text_classes'])+" to be in Image Classes "+str(possible_texts))
