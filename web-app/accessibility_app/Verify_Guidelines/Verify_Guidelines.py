import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))
from Image_Detection import DetectObj
from TextAnalyzer import DetectText


class Verify_Guidelines:
    def ExtractClasses(self, url, alt, relevance):
        classes = {}
        detectImg = DetectObj.DetectObj()
        classesFromImage = detectImg.detect_Object_from_API(url)
        classes["image_classes"] = classesFromImage
        detectText = DetectText.DetectText()
        classesFromText = detectText.detectTextIn(alt)
        classes["text_classes"] = classesFromText
        classes["relevant"] = False
        for item in classes["text_classes"]:
            if item in classes["image_classes"]:
                classes["relevant"] = True
        return classes
