from imageai.Prediction import ImagePrediction
import os
import sys
execution_path=os.getcwd()
path=execution_path
sys.path.append(path)
Model_dir_Path= os.path.dirname(os.path.realpath(__file__))
Web_app_dir=os.path.dirname(os.path.realpath(__file__+"../../.."))
from Image_Detection.ImageSaver import ImageSave
import re
from imageai.Prediction.Custom import CustomImagePrediction

class Predict_Image:
    
    # other model to be trained 
    def __init__(self,Threshold=20,modelName="ResNet",CustomModelName=None,CustomModelJsonFilePath=None):
        self.Threshold=Threshold
        if CustomModelName is None:
            self.prediction = ImagePrediction()
        else:
            self.prediction = CustomImagePrediction()
        
        if modelName in "ResNet":
            self.prediction.setModelTypeAsResNet()
            if CustomModelName is None:
                self.prediction.setModelPath(Model_dir_Path+"/Models/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
            else:
                self.prediction.setModelPath(Model_dir_Path+"/Models/"+CustomModelName)
                prediction.setJsonPath(Model_dir_Path+"/Models/"+CustomModelJsonFilePath)
        
            
        elif modelName in "SqueezeNet":
            self.prediction.setModelTypeAsSqueezeNet()
            if CustomModelName is None:
                self.prediction.setModelPath(Model_dir_Path+"/Models/squeezenet_weights_tf_dim_ordering_tf_kernels.h5")
            else:
                self.prediction.setModelPath(Model_dir_Path+"/Models/"+CustomModelName)
                prediction.setJsonPath(Model_dir_Path+"/Models/"+CustomModelJsonFilePath)
        elif modelName in "InceptionV3":
            self.prediction.setModelTypeAsInceptionV3()
            if CustomModelName is None:
                self.prediction.setModelPath(Model_dir_Path+"/Models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5")
            else:
                self.prediction.setModelPath(Model_dir_Path+"/Models/"+CustomModelName)
                prediction.setJsonPath(Model_dir_Path+"/Models/"+CustomModelJsonFilePath)            
        elif modelName in "DenseNet" :
            self.prediction.setModelTypeAsDenseNet()
            if CustomModelName is None:
                self.prediction.setModelPath(Model_dir_Path+"/Models/DenseNet-BC-121-32.h5")
            else:
                self.prediction.setModelPath(Model_dir_Path+"/Models/"+CustomModelName)
                prediction.setJsonPath(Model_dir_Path+"/Models/"+CustomModelJsonFilePath) 
            
        
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
    
