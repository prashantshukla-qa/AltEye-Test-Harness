from lxml import html

class Image_html_parser:
    def __init__(self,page_content):
        self.tree = html.fromstring(page_content)

    def get_Images_alt_vicinity(self):
        ImageElement=self.tree.xpath("//img")
        ImageElementParent=self.tree.xpath("//img/..")
        list_of_Image=[]
        for element,parentElement in zip(ImageElement,ImageElementParent):
            if parentElement.tag=="body":
                vicinityText=""
            elif parentElement.tag=="figure":
                vicinityText=parentElement.text_content()
            else:
                vicinityText=parentElement.text_content()
            list_of_Image.append([element.get("src"),element.get("alt"),vicinityText])
        return list_of_Image
        
