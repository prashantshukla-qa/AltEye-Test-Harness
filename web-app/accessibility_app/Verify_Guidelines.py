from Image_Detection import Image_Data_Scanner
from TextAnalyzer import DetectText
from Image_AI import Image_prediction


class Verify_Guidelines:

    def ExtractClasses(self, url, alt, vicinity_text, Threshold=80, model="DenseNet",CustomModel=None,CustomJson=None):

        self.detectText = DetectText.DetectText()

        classes = {}
        #initalizing the Image_has_text boolean var
        Image_has_Text = False;
        self.scan_Image = Image_Data_Scanner.Image_Scanner(Threshold)
        list_of_entities = self.scan_Image.Scan_Image(url)
        Image_has_Text = self.scan_Image.is_Text_Present_In_Image()
        #self.scan_Image_via_Image_AI = Image_prediction.Predict_Image(Threshold, model,CustomModel,CustomJson)
        #print("Now using ImageAI API to detect Image")
        #list_of_entities=list_of_entities +self.scan_Image_via_Image_AI.get_classes_from_image(url)
        
        ##Detecting text from alt text 
        classesFromText = self.detectText.detectTextIn(alt)
        #now list_of_entities has 
        classes["possible_texts"] = []
        classes["result"] = False
        ## Checking if Image has text
        if Image_has_Text:
            classes["text_classes"]=classesFromText
            ## converted the text classes into small case
            for text in self.scan_Image.get_Text_list_From_Image():
                classes["possible_texts"].append(text)
                for text_in_text_class in classes["text_classes"]:
                    if text["Entity"].lower() in text_in_text_class.lower():
                        classes["result"] = "GREEN"
                else: 
                    for exact_text in classes["text_classes"]:
                        if text["Entity"].lower() in exact_text.lower():
                            classes["result"] = "GREEN"
        

        ##Detecting text from vicinity text 
        classesFromVicinityText=self.detectText.detectTextIn(vicinity_text)
        
        result_check_for_vicinity="RED"

        if not alt:  
            classes["text_classes"] = [x.lower() for x in classesFromVicinityText]
            for item in list_of_entities:
                classes["possible_texts"].append(item)
                if item["Entity"] in classes["text_classes"]:
                   result_check_for_vicinity = "GREEN"
              
            if result_check_for_vicinity == "GREEN":
                classes["result"] = "alt text was not found but caption may convey the image information "
            else:
                classes["result"] = "alt text was not found and  caption may not be convying the image information "

        classes["text_classes"] = classesFromText
        for item in list_of_entities:
            classes["possible_texts"].append(item)
            for text_in_text_class in classes["text_classes"]:
                image_class=item["Entity"]
                if "(Web-Entity)" in image_class:
                    image_class=image_class.replace(" (Web-Entity)","")
                # print("comparing",text_in_text_class,"and",image_class)
                if text_in_text_class.lower() in image_class.lower():
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
        return classes
