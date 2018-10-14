from Image_Detection import Image_Data_Scanner
from TextAnalyzer import DetectText
from Image_AI import Image_prediction

class Verify_Guidelines:

    def ExtractClasses(self, url, alt, vicinity_text,method="googleAPI",Threshold=80,model="DenseNet"):
        self.scan_Image = Image_Data_Scanner.Image_Scanner(Threshold)
        self.detectText = DetectText.DetectText()
        self.scan_Image_via_Image_AI=Image_prediction.Predict_Image(Threshold,model)
        classes = {}
        if method in "googleAPI":
            print("using google API")
            list_of_entities = self.scan_Image.Scan_Image(url)
        else:
            print("using ImageAI API")
            list_of_entities = self.scan_Image_via_Image_AI.get_classes_from_image(url)
        
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


# print(Verify_Guidelines().ExtractClasses(
#     "https://upload.wikimedia.org/wikipedia/commons/thumb//f/f4/Honeycrisp.jpg/220px-Honeycrisp.jpg",
#     "Honeyshit", "",""))
