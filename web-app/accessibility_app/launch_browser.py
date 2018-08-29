from selenium import webdriver
from urllib import request


class PageParser:

    def __init__(self, browser, url):
        chromedriver = "drivers/chromedriver"
        self.driver = webdriver.Chrome(chromedriver)
        self.launch_browser(browser, url)

    def launch_browser(self, browser, url):

        if (url.startswith('http://') or url.startswith('https://')):
            self.driver.get(url)
        else:
            self.driver.get('http://' + url)

    def getImagesAndAltText(self):
        image_details = {}
        image_elements = self.driver.find_elements_by_tag_name('img')
        for index, element in enumerate(image_elements):
            if (element.is_displayed()):
                image_details[str(index)] = \
                    {"src": element.get_attribute("src"),
                     "alt": element.get_attribute("alt"),
                     "vicinity_text": element.find_element_by_xpath('..').text}
                request.urlretrieve(image_details[str(index)]["src"],
                                    "./web-app/static/images/" +
                                    "retrieved_images/" +
                                    "image_" + str(index) + ".jpg")
        return image_details
