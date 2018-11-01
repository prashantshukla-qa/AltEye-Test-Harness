import unittest
from selenium import webdriver
from automation_tool.VicinityElements import GetVicinityText
from automation_tool.ImageWebdriver import Image_Chrome_Webdriver

class SeleniumTest():

    def test_Hello(self):
        image_details = {}
        driver = Image_Chrome_Webdriver()
        driver.get("https://en.wikipedia.org/wiki/Car")
        image_elements = driver.find_elements_by_tag_name('img')

        for index, element in enumerate(image_elements):
            if (element.is_displayed()):
                image_details[str(index)] = \
                    {"src": element.get_attribute("src"),
                        "alt": element.get_attribute("alt"),
                        "vicinity_text": GetVicinityText.get_vicinity_text(element,1)
                    }
                driver.Test_Alt_Text_Relevancy(image_details[str(index)]['src'],image_details[str(index)]['alt'],image_details[str(index)]['vicinity_text'])        
        
if __name__ == '__main__':
    SeleniumTest().test_Hello()
