from selenium import webdriver


class GetVicinityText:
    @staticmethod
    def get_vicinity_text(element,level=3):
        text=None
        i=0
        while not text or i<level:
            parent_element=element.find_element_by_xpath('..')
            text=parent_element.text
            i=i+1
            element=parent_element
            if parent_element.tag_name in "body":
                break
        
        return text
            



driver = webdriver.Chrome()
driver.get("https://www.bell-labs.com/usr/dmr/www/")
print(GetVicinityText.get_vicinity_text(driver.find_element_by_xpath('//img[@alt="DMR picture"]')))
