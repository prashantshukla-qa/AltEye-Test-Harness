
from imageai.Prediction import ImagePrediction
import os
import sys
execution_path=os.getcwd()
path=execution_path
#sys.path.append(path)
# sys.path.append("/home/jaspal/Desktop/accessibility-test/web-app/accessibility_app/Image_Detection/")
# sys.path.append("/home/jaspal/Desktop/accessibility-test/web-app/accessibility_app/")
# print(sys.path)
from Image_Detection.ImageSaver import ImageSave
import re
from imageai.Prediction.Custom import CustomImagePrediction

class Predict_Image:


    # other model to be trained 
    def __init__(self,Threshold=20,modelName="DenseNet",CustomModelName=None,CustomModelJsonFilePath=None):
        global Model_dir_Path, Web_app_dir
        Model_dir_Path= os.path.dirname(os.path.realpath(__file__))
        Web_app_dir=os.path.dirname(os.path.realpath(__file__+"../../.."))
        self.Threshold=Threshold
        print("Here ....3\n")
        if CustomModelName is None:
            print("Here ....4\n")
            self.prediction = ImagePrediction()
        else:
            self.prediction = CustomImagePrediction()
        
        if modelName in "ResNet":
            print("Here ....5\n")
            self.prediction.setModelTypeAsResNet()
            if CustomModelName is None:
                self.prediction.setModelPath(Model_dir_Path+"/Models/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
            else:
                self.prediction.setModelPath(Model_dir_Path+"/Models/"+CustomModelName)
                self.prediction.setJsonPath(Model_dir_Path+"/Models/"+CustomModelJsonFilePath)
        
            
        elif modelName in "SqueezeNet":
            print("Here ....5\n")
            self.prediction.setModelTypeAsSqueezeNet()
            if CustomModelName is None:
                self.prediction.setModelPath(Model_dir_Path+"/Models/squeezenet_weights_tf_dim_ordering_tf_kernels.h5")
            else:
                self.prediction.setModelPath(Model_dir_Path+"/Models/"+CustomModelName)
                self.prediction.setJsonPath(Model_dir_Path+"/Models/"+CustomModelJsonFilePath)

        elif modelName in "InceptionV3":
            print("Here ....6\n")
            self.prediction.setModelTypeAsInceptionV3()
            if CustomModelName is None:
                self.prediction.setModelPath(Model_dir_Path+"/Models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5")
            else:
                self.prediction.setModelPath(Model_dir_Path+"/Models/"+CustomModelName)
                self.prediction.setJsonPath(Model_dir_Path+"/Models/"+CustomModelJsonFilePath)   

        elif modelName in "DenseNet" :
            print("Here ....7\n")
            self.prediction.setModelTypeAsDenseNet()
            if CustomModelName is None:
                print("Here ....7.3\n")
                print("value of Model Dir is"+Model_dir_Path+"/Models/DenseNet-BC-121-32.h5"+"\n")
                self.prediction.setModelPath(Model_dir_Path+"/Models/DenseNet-BC-121-32.h5")
            else:
                rint("Here ....8\n")
                self.prediction.setModelPath(Model_dir_Path+"/Models/"+CustomModelName)
                self.prediction.setJsonPath(Model_dir_Path+"/Models/"+CustomModelJsonFilePath) 
        self.prediction.loadModel()

    def get_classes_from_image(self,url):
        save_Image=ImageSave()
        self.name=os.path.basename(url)
        save_Image.save_Image_from_url(url,self.name)
        predictions, probabilities = self.prediction.predictImage(Web_app_dir+"/static/images/retrieved_images/"+self.name, result_count=10 )
        result_set = []
        for eachPrediction, eachProbability in zip(predictions, probabilities):
            if eachProbability > self.Threshold:
                result_set.append({'Entity': eachPrediction,
                     'confidence': round(eachProbability,2)})
                print(eachPrediction,eachProbability)
        return result_set

    def setModel(self,modelName):
        if modelName in "ResNet":
            self.prediction.setModelTypeAsResNet()
            self.prediction.setModelPath(Model_dir_Path+"/Models/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
        elif modelName in "SqueezeNet":
            self.prediction.setModelTypeAsSqueezeNet()
            self.prediction.setModelPath(Model_dir_Path+"/Models/squeezenet_weights_tf_dim_ordering_tf_kernels.h5")

        elif modelName in "InceptionV3":
            self.prediction.setModelTypeAsInceptionV3()
            self.prediction.setModelPath(Model_dir_Path+"/Models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5")
        elif modelName in "DenseNet" :
            self.prediction.setModelTypeAsDenseNet()
            self.prediction.setModelPath(Model_dir_Path+"/Models/DenseNet-BC-121-32.h5")
        self.prediction.loadModel()
    

