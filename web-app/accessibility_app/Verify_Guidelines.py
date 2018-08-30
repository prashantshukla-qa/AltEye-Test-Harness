from Image_Detection import Image_Data_Scanner
from TextAnalyzer import DetectText


class Verify_Guidelines:
    scan_Image = Image_Data_Scanner.Image_Scanner(80)
    detectText = DetectText.DetectText()

    def ExtractClasses(self, url, alt, relevance):
        classes = {}
        list_of_entities = self.scan_Image.Scan_Image(url)
        classesFromText = self.detectText.detectTextIn(alt)
        classes["possible_texts"] = []
        classes["text_classes"] = classesFromText
        classes["result"] = False
        for item in list_of_entities:
            classes["possible_texts"].append(item)
            if item["Entity"] in classes["text_classes"]:
                classes["result"] = "GREEN"
        if classes["result"] is False:
            classes["result"] = "RED"
        return classes


print(Verify_Guidelines().ExtractClasses(
    "https://upload.wikimedia.org/wikipedia/commons/thumb\
    /f/f4/Honeycrisp.jpg/220px-Honeycrisp.jpg",
    "Honeycrisp", ""))
