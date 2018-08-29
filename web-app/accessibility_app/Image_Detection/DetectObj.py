import cv2
from clarifai.rest import ClarifaiApp


class DetectObj:

    def __init__(self, Haarfile="/HaarFiles/face.xml"):
        self.HaarfilePath = Haarfile
        app = ClarifaiApp(api_key='dc1938142dcd4ed59067fb07e223f0d6')
        self.model = app.public_models.general_model

    def detect_Object_from_haar(self, image):
        haarfile = self.HaarfilePath
        faceCascade = cv2.CascadeClassifier(haarfile)
        # Read the image
        image = cv2.imread(image)
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except:
            return
        matchs = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        print("Found {0} Match!".format(len(matchs)))

        # Draw a rectangle around the faces
        for (x, y, w, h) in matchs:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if len(matchs) == 0:
            return False
        else:
            cv2.imwrite('Images/MatchFound.png', image)
            return True

    def detect_Object_from_API(self, src):
        classlist = []
        response = self.model.predict_by_url(url=src)
        concepts = response['outputs'][0]['data']['concepts']
        for concept in concepts:
            print(concept['name'], concept['value'])
            if(concept['value']*100 > 90.00):
                classlist.append(concept['name'])
        return classlist
