import unittest
from accessibility_app.launch_browser import PageParser
from selenium import webdriver


class SeleniumTest(unittest.TestCase):

    def test_image_details(self):
        image_details = {}

        driver = PageParser(
            "chrome", "https://en.wikipedia.org/wiki/Tiger")\
            .launch_browser()

        image_elements = driver.find_elements_by_tag_name('img')

        for index, element in enumerate(image_elements):
            if (element.is_displayed()):
                image_details[str(index)] = \
                    {"src": element.get_attribute("src"),
                        "alt": element.get_attribute("alt"),
                        "vicinity_text": element.find_element_by_xpath
                        ("../../..").text}
            if (index == 6):
                print(element.find_element_by_xpath
                      ("../../..").text)
