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
            


