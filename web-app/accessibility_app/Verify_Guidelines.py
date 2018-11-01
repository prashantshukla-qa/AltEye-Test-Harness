from Image_Detection import Image_Data_Scanner
from TextAnalyzer import DetectText
from Image_AI import Image_prediction


class Verify_Guidelines:

    def ExtractClasses(self, url, alt, vicinity_text, method="googleAPI", Threshold=80, model="DenseNet"):

        self.detectText = DetectText.DetectText()

        classes = {}
        if method in "googleAPI":
            self.scan_Image = Image_Data_Scanner.Image_Scanner(Threshold)
            print("using google API")
            list_of_entities = self.scan_Image.Scan_Image(url)
            Image_has_Text = self.scan_Image.is_Text_Present_In_Image()
        else:
            self.scan_Image_via_Image_AI = Image_prediction.Predict_Image(
                Threshold, model)
            print("using ImageAI API")
            list_of_entities = self.scan_Image_via_Image_AI.get_classes_from_image(
                url)
            Image_has_Text = False
        classes["possible_texts"] = []
        classes["result"] = False
        if Image_has_Text:
            classes["text_classes"]=alt.lower().split()
            for text in self.scan_Image.get_Text_list_From_Image():
                classes["possible_texts"].append(text)
                if (text["Entity"].lower() in classes["text_classes"]):
                    classes["result"] = "GREEN"
                else: 
                    for exact_text in classes["text_classes"]:
                        if text["Entity"].lower() in exact_text:
                            classes["result"] = "GREEN"
        classesFromText = self.detectText.detectTextIn(alt)
        classes["text_classes"] = classesFromText
        for item in list_of_entities:
            classes["possible_texts"].append(item)
            if item["Entity"] in classes["text_classes"]:
                classes["result"] = "GREEN"
        
        if classes["result"] is False:
            classes["result"] = "RED"
        unique_lists=[]
        unique_keys=[]
        for item in classes["possible_texts"]:
            if item['Entity'].lower() in [x.lower() for x in unique_keys]:
                pass
            else:
                unique_keys.append(item['Entity'])
                unique_lists.append(item)
        classes["possible_texts"]=unique_lists
        print(classes["possible_texts"])
        return classes
