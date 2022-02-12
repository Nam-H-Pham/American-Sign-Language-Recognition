import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import os
import xlrd
import cv2
import HandDataCollecter
import mediapipe as mp
import numpy as np

########Initialise random forest

local_path = (os.path.dirname(os.path.realpath('__file__')))

file_name = ('ASL-Data.csv')#file of total data
data_path = os.path.join(local_path,file_name)
print (data_path)
df = pd.read_csv(r''+data_path)

print (df)

units_in_data = 28 #no. of units in data

titles = []
for i in range(units_in_data):
    titles.append("unit-"+str(i))
X = df[titles]
y = df['letter']


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.5,random_state=2)

clf = RandomForestClassifier(n_estimators=30)#random forest
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
print('Accuracy: ',metrics.accuracy_score(y_test, y_pred))

#########Begin predictions
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def get_prediction(image):
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        ImageData = HandDataCollecter.ImageToDistanceData(image, hands)
        DistanceData = ImageData['Distance-Data']
        image = ImageData['image']
        prediction = clf.predict([DistanceData])
        return prediction[0]


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    SpelledWord = ""
    while cap.isOpened():
            success, image = cap.read()
            if not success:
                        print("Ignoring empty camera frame.")
                        # If loading a video, use 'break' instead of 'continue'.
                        continue

            '''ImageData = HandDataCollecter.ImageToDistanceData(image, hands)
            DistanceData = ImageData['Distance-Data']
            image = ImageData['image']

            if cv2.waitKey(1) & 0xFF == 32:
                prediction = clf.predict([DistanceData])
                SpelledWord = str(prediction[0])
                #print(SpelledWord)'''

            try:
                SpelledWord = get_prediction(image)
                #cv2.putText(image,  SpelledWord, (50,50), 1, 2, 255)
                cv2.putText(image,SpelledWord,(50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            except:
                pass



            cv2.imshow('frame', image)
                
            if cv2.waitKey(5) & 0xFF == 27: #press escape to break
                        break
    
    cap.release()
    cv2.destroyAllWindows()
