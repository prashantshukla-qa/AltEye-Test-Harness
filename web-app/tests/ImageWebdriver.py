from selenium import webdriver
import urllib.request
import os
SERVER_URL = "http://localhost:5000"
import json


class Image_Chrome_Webdriver(webdriver.Chrome):
    print("here2")
    def __init__(self,executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):

                 super().__init__(executable_path, port,options, service_args,desired_capabilities, service_log_path,
                 chrome_options, keep_alive)

    
    def Test_Alt_Text_Relevancy(self,url, alt, vicinity, method="googleAPI", model="DenseNet", Threshold=30):
        url_Complete=SERVER_URL+"/api/get_alt_relevancy/?url="+url+"&alt="+alt+"&vicinity="+vicinity+"&method="+method+"&model="+model+"&Threshold="+str(Threshold)
        Response = urllib.request.urlopen(url_Complete)
        json_acceptable_string=Response.read().decode('utf-8')
        Result=json.loads(json_acceptable_string)
        possible_texts=[x['Entity'] for x in Result['possible_texts']]
        assert Result['result']=="GREEN","Expected the Text classes"+str(Result['text_classes'])+" to be in Image Classes "+str(possible_texts)     
        
