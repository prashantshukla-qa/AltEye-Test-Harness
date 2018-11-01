from imageai.Prediction.Custom import ModelTraining
import os 
path=os.path.dirname(os.path.realpath(__file__))


class Custom_Train:

    @staticmethod
    def train_model(foldername,Model_Type,num_objects=2, num_experiments=1, enhance_data=False, batch_size=1, show_network_summary=True):
        model_trainer = ModelTraining()
        if Model_Type in "ResNet":
            model_trainer.setModelTypeAsResNet()
        elif Model_Type in "SqueezeNet":
            model_trainer.setModelTypeAsSqueezeNet()
        elif Model_Type in "InceptionV3":
            model_trainer.setModelTypeAsInceptionV3()
        elif Model_Type in "DenseNet":
            model_trainer.setModelTypeAsDenseNet()
        model_trainer.setDataDirectory(foldername)
        model_trainer.trainModel(num_objects=num_objects, num_experiments=num_experiments, enhance_data=enhance_data, batch_size=batch_size, show_network_summary=show_network_summary)
