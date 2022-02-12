import cv2
import mediapipe as mp
import math
import pickle
import os
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

Position_Layers = [
            [0],
            [1,5,9,13,17],
            [2,6,10,14,18],
            [3,7,11,15,19],
            [4,8,12,16,20],
        ]

def GetPositionLayer(HandIndex):
    for layernum, line in enumerate(Position_Layers):
        if HandIndex in line:
            return {
                'layer': layernum,
             'index': line.index(HandIndex)
             }

def GetPointsDistance(p1,p2):
    return math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )

def GetRelativeDistance(StandardLength, p1, p2):
    PointDistance = GetPointsDistance(p1, p2)
    return PointDistance/StandardLength

def ImageToDistanceData(image, hands):
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    Frame_Layer_Data = [
        [],
        [],
        [],
        [],
    ]

    Hand_Frame_Data = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            for index, landmark in enumerate(hand_landmarks.landmark):
                x = landmark.x
                y = landmark.y
                z = landmark.y

                shape = image.shape
                relative_x = int(x * shape[1])
                relative_y = int(y * shape[0])
                
                Hand_Frame_Data.append([relative_x, relative_y])

                #cv2.putText(image,  str(GetPositionLayer(index)['layer']), (relative_x,relative_y), 0, 0.5, 255)
            break

    DistanceData = []
    if len(Hand_Frame_Data) > 0:
        StandardLength = GetPointsDistance(Hand_Frame_Data[0], Hand_Frame_Data[5])

        for layerindex, layer in enumerate(Position_Layers):
            for sublayerindex, handindex in enumerate(layer):

                point = Hand_Frame_Data[Position_Layers[layerindex][sublayerindex]]

                if layerindex > 1: #get distance from one below, make exception for wrist
                    BelowLayerPoint = Hand_Frame_Data[Position_Layers[layerindex-1][sublayerindex]]
                    
                    RelativeLength = GetRelativeDistance(StandardLength, point, BelowLayerPoint)
                    #cv2.putText(image,  str(round(RelativeLength, 2)), (point), 0, 0.5, 255)

                    colour = (RelativeLength/0.3) * 255
                    if colour > 255: colour = 255
                    #cv2.line(image, (point), (BelowLayerPoint), (0, colour, 0), thickness=3)

                    DistanceData.append(RelativeLength)
                
                if layerindex == 4: #get distance from fingertip to palm
                    RelativeLength = GetRelativeDistance(StandardLength, point, Hand_Frame_Data[0])

                    colour = (RelativeLength/0.6) * 255
                    if colour > 255: colour = 255
                    #cv2.line(image, (point), (Hand_Frame_Data[0]), (0, colour, 0), thickness=3)

                    DistanceData.append(RelativeLength)

                    if sublayerindex < 4: # get distances between fingertips
                        NeighbourPoint = Hand_Frame_Data[Position_Layers[layerindex][sublayerindex+1]]
                        RelativeLength = GetRelativeDistance(StandardLength, point, NeighbourPoint)

                        #cv2.putText(image,  str(round(RelativeLength, 2)), (point), 0, 0.5, 255)

                        #colour = (RelativeLength/0.6) * 255
                        #if colour > 255: colour = 255
                        #cv2.line(image, (point), (NeighbourPoint), (0, colour, 0), thickness=3)

                        DistanceData.append(RelativeLength)

                if layerindex == 4: #distance from thumb tip to fingertip
                    if sublayerindex > 0:
                        RelativeLength = GetRelativeDistance(StandardLength, point, Hand_Frame_Data[4])

                        #colour = (RelativeLength/0.6) * 255
                        #if colour > 255: colour = 255
                        #cv2.line(image, (point), (Hand_Frame_Data[4]), (0, colour, 0), thickness=3)

                        DistanceData.append(RelativeLength)
                    


    return {
        'Distance-Data': DistanceData,
        'image': image
    }


if __name__ == '__main__':
    ChosenLetter = input("Letter: ")
    ChosenLetter = ChosenLetter.upper()
    PKL_PATH = os.path.join(os.path.join((os.path.dirname(os.path.realpath('__file__'))),"ASL Pickles"),(ChosenLetter + '-dataset.pkl'))
    
    timeline = []
    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            
            ImageData = ImageToDistanceData(image, hands)
            DistanceData = ImageData['Distance-Data']
            image = ImageData['image']

            if cv2.waitKey(1) & 0xFF == 32: #space key is pressed (add distance data to timeline)
              cv2.putText(image,  "Recording", (50,50), 0, 0.5, 255)
              timeline.append(DistanceData)

            if len(timeline) > 100: #given 100 frames of data, save to pickle and release
                with open(PKL_PATH, 'wb') as f:
                    pickle.dump(timeline, f)
                break

            cv2.imshow("MediaPipe Hands", image)
            if cv2.waitKey(5) & 0xFF == 27: #press escape to break
                break
            
    cap.release()
