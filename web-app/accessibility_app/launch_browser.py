from selenium import webdriver
from urllib import request
from selenium.webdriver.chrome.options import Options
import time
from accessibility_app.Image_Detection.Image_Data_Scanner import Image_Scanner
from accessibility_app.TextAnalyzer.DetectText import DetectText


class PageParser:

    def __init__(self, browser, url):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.browser = browser
        self.url = url

    def launch_browser(self):

        if (self.url.startswith('http://') or self.url.startswith('https://')):
            self.driver.get(self.url)
        else:
            self.driver.get('http://' + self.url)
        return self

    def get_images_and_alt_text(self):
        image_details = {}
        image_elements = self.driver\
            .find_element_by_class_name('infobox')\
            .find_elements_by_tag_name('img')

        if image_elements.__len__() == 0:
            pass

        for index, element in enumerate(image_elements):
            if (element.is_displayed()) and element.size['height'] > 25:
                image_details[str(index)] = \
                    {"src": element.get_attribute("src"),
                     "alt": element.get_attribute("alt"),
                     "vicinity_text": element.size['height'],
                     #  "vicinity_text": element.find_element_by_xpath
                     #  ("../../..").text,
                     "current_time": time.time()}
                request.urlretrieve(image_details[str(index)]["src"],
                                    "./static/images/" +
                                    "retrieved_images/" +
                                    "image_" + str(index) + ".jpg")
        return image_details

    def get_vision_feedback(self):
        image_details = self.get_images_and_alt_text()
        for index, element in enumerate(image_details):
            classes = {}
            list_of_entities = Image_Scanner(80)\
                .Scan_Image(image_details[str(index)]["src"])
            classesFromText = DetectText()\
                .detectTextIn(image_details[str(index)]["src"])
            classes["possible_texts"] = []
            classes["text_classes"] = classesFromText
            classes["result"] = False
            for item in list_of_entities:
                classes["possible_texts"].append(item)
                if item["Entity"] in classes["text_classes"]:
                    classes["result"] = "GREEN"
                if classes["result"] is False:
                    classes["result"] = "RED"
            image_details[str(index)]['classes'] = classes
        return image_details

    def get_driver_instance(self):
        return self.driver
