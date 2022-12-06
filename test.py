import cv2 
import mediapipe as mp
import math
import numpy as np
import serial
import time
import os
from stitcher import Stitcher

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1) 
mp_drawing = mp.solutions.drawing_utils #used for visualising our drawings

# serialcomm = serial.Serial('COM5', 9600)
# serialcomm.timeout = 1

cap = cv2.VideoCapture(0) # Replace with your own video and webcam
file_directory = "C:/Users/Kridbhume Chammanard/Desktop/Robotic Project I"
image_directory = "C:/Users/Kridbhume Chammanard/Desktop/Robotic Project I/images"

os.chdir(image_directory)

def countPlayers(name):
    ret,frame = cap.read()
    #serialcomm.write("rotate".encode())
    time.sleep(0.5)
    cv2.imshow("frame", frame)
    if ret:
        cv2.imwrite(name,frame)


def coordinate(id, h, w):
    cx, cy = lm.x*w, lm.y*h
    cv2.circle(img, (int(cx), int(cy)), 1, (255,255,255), cv2.FILLED)  
    return cx, cy

def distance(cx1,cy1,cx2,cy2):
    return math.sqrt(((cx2-cx1)**2) + ((cy2-cy1)**2))
    
for i in range(7):
    time.sleep(2)
    countPlayers("image {}.jpg".format(i))

os.remove("image 0.jpg")
os.chdir(file_directory)

while True:
    success, img = cap.read()
    
    if not success: 
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    h, w, c = img.shape
    next_turn = 0
    draw_card = 0
    invalid = 0
    serialinput = 0
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                if id == 0: 
                    __, cy_0 = coordinate(0, h, w)
                if id == 10: 
                    __, cy_10 = coordinate(10, h, w)
            
                if id == 2:
                    __, cy_2 = coordinate(2, h, w)
                if id == 3:
                    __, cy_3 = coordinate(3, h, w)
                if id == 1:
                    cx_1, cy_1 = coordinate(1, h, w)
                if id == 4:
                    cx_4, cy_4 = coordinate(4, h, w)
            
                if id == 5: 
                    cx_5, cy_5 = coordinate(5, h, w)
                if id == 9: 
                    __, cy_9 = coordinate(9, h, w)
                if id == 13: 
                    __, cy_13 = coordinate(13, h, w)
                if id == 17: 
                    cx_17, cy_17 = coordinate(17, h, w)
                    
                if id == 8: 
                    __, cy_8 = coordinate(8, h, w)  
                if id == 12: 
                    __, cy_12 = coordinate(12, h, w)
                if id == 16: 
                    __, cy_16 = coordinate(16, h, w)
                if id == 20: 
                    __, cy_20 = coordinate(20, h, w)

                if id == 6:
                    cx_6, cy_6 = coordinate(6, h, w)
            
            if (cy_5 > cy_8) and (cy_13 < cy_16 and cy_17 < cy_20 and cy_9 < cy_12):
                draw_card = 1
                serialinput = 1
            else:
                draw_card = 0
                serialinput = 0
            
            if (cy_5 > cy_8 and cy_9 > cy_12) and (cy_13 < cy_16 and cy_17 < cy_20):
                next_turn = 1
                serialinput = 1
            else:
                next_turn = 0
                serialinput = 0

            if draw_card == next_turn:
                invalid = 1
                cv2.putText(img,"INVALID",(15,12),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)        
            
            else:
                invalid = 0


    if draw_card == 1:
        cv2.putText(img,"DRAW CARD",(15,12),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)

    if next_turn == 1:
        cv2.putText(img,"NEXT TURN",(15,12),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)

    cv2.imshow("Image", img)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break  

#serialcomm.close()

cap.release()
cv2.destroyAllWindows()