from selenium import webdriver
from urllib import request
from selenium.webdriver.chrome.options import Options
import time
from accessibility_app.Image_Detection.Image_Data_Scanner import Image_Scanner
from accessibility_app.TextAnalyzer.DetectText import DetectText
from accessibility_app.Verify_Guidelines import Verify_Guidelines
import re


class PageParser:

    def __init__(self, browser, url):
        options = webdriver.ChromeOptions()
      #  options.add_argument("headless")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.browser = browser
        self.url = url

    def launch_browser(self):

        if (self.url.startswith('http://') or self.url.startswith('https://')):
            self.driver.get(self.url)
        else:
            self.driver.get('http://' + self.url)
        return self

    def get_images_and_alt_text(self,width=50,height=50):
        image_details = []
        image_elements = self.driver.find_elements_by_xpath('//img')
        iframes = self.driver.find_elements_by_xpath('//iframe')
        for index, iframe in enumerate(iframes):
                self.driver.switch_to.frame(iframe)
                frame_image_details=self.driver.find_elements_by_xpath('//img')
                image_elements+frame_image_details
                self.driver.switch_to.parent_frame()
        print(image_elements)
        if image_elements.__len__() == 0:
            pass

        index = 0
        for index_bak, element in enumerate(image_elements):
                if (element.is_displayed()) and element.size['height'] > height and element.size['width'] > width: 
                    print(element.get_attribute("src")) 
                    image_details.append(\
                        {"src": element.get_attribute("src"),
                            "alt": element.get_attribute("alt"),
                            "vicinity_text": element.find_element_by_xpath("..").text,
                            "current_time": time.time()})
        return image_details

    def get_vision_feedback(self,model=1,Threshold=60,width=50,height=50):
        image_details = self.get_images_and_alt_text(width,height)
        modelDict={"1":"DenseNet","2":"ResNet","3":"SqueezeNet","4":"InceptionV3"}

        for index, element in enumerate(image_details):
            classes = {}
            image_details[index]["alt"] = re.sub(
                "\.(\w+)$", "", image_details[index]["alt"])
            print(index)
            classes = Verify_Guidelines().ExtractClasses(image_details[index]["src"], image_details[
                index]["alt"],image_details[index]["vicinity_text"],Threshold,modelDict[str(model)])
            image_details[index]['classes'] = classes
        return image_details
    def get_driver_instance(self):
        return self.driver
