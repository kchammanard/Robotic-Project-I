
 
#################### IMPORT LIBRARIES ####################
import cv2 
import mediapipe as mp
import math
import numpy as np
import serial
import time
import os
import HandTrackingModule as htm

################# INSTANTIATE VARIABLES #################
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1,min_detection_confidence = 0.8,min_tracking_confidence = 0.8) 
mp_drawing = mp.solutions.drawing_utils #used for visualising our drawings

serialcomm = serial.Serial('COM3', 9600)
serialcomm.timeout = 1

#################### COUNT PLAYERS ####################
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


def coordinate(id, h, w):
    cx, cy = lm.x*w, lm.y*h
    cv2.circle(img, (int(cx), int(cy)), 1, (255,255,255), cv2.FILLED)  
    return cx, cy

def distance(cx1,cy1,cx2,cy2):
    return math.sqrt(((cx2-cx1)**2) + ((cy2-cy1)**2))

def count_players():

    time_count = 0
    current_finger = 99
    previous_finger = 0
    pTime = 0
    tipIds = [4, 8, 12, 16, 20]
    timeout = time.time() + 3
    detector = htm.handDetector(detectionConf=0.75)

    while True:
        previous_finger = current_finger
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            fingers = []
            # * for right hand front only
            # * thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for idx in range(1, 5):
                if lmList[tipIds[idx]][2] < lmList[tipIds[idx] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            count = 0

            for i in fingers:
                if i == 1:
                    count += 1

            if count != 0:
                #print(f"The number of players is {count}")
                angle_per_player = 360 / count
                #print(angle_per_player)
                current_finger = count

            cv2.putText(img, f"WAIT {int(time_count/10)}/5", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            if count != 1:
                cv2.putText(img, f"{count} fingers", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            else:
                cv2.putText(img, "1 finger", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        if current_finger == previous_finger and len(lmList) != 0:
            time_count += 1
        else: time_count = 0

        cv2.putText(img, f"FPS: {int(fps)}", (450, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord("q") or (time_count == 50 and current_finger != 99): #or time.time() > timeout:
            break

    if count == 0 or count == 1:
        count_players()
    else: 
        print(f"The number of players is {count}")
    return count

def startingCards(i, j):
    if i == int(num_players) and j == 0:
        serialcomm.write("reset".encode())
        time.sleep(2)
    serialcomm.write("shoot card".encode())
    time.sleep(2)
    print(serialcomm.readline().decode('ascii'))
    serialcomm.write("next turn".encode())
    time.sleep(2)
    print(serialcomm.readline().decode('ascii'))
    
count = count_players()
cap.release()
cv2.destroyAllWindows()

#################### INPUT NUMBER OF PLAYERS  ####################

num_players = str(count)
serialcomm.write(num_players.encode())
print(serialcomm.readline().decode('ascii'))

#################### INITIATE GAME ####################

cap = cv2.VideoCapture(0) # Replace with your own video and webcam
file_directory = "C:/work/year 2/robotic project/Robotic Project I"
image_directory = "C:/work/year 2/robotic project/Robotic Project I/images"

turn_used = 0
cards_left = 52

players = [str(n) for n in range(1, int(num_players) + 1)]

for i in range(int(num_players)+1):
    j = i % int(num_players)
    print(i, j, "Starting")
    startingCards(i, j)
# #     players.append(f"Player {i+1}")
# print(players)

iterator = 0

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
        print(f"Currently Player {players[iterator]}'s turn")
        if iterator == len(players) - 1:
            iterator = 0
        else:
            iterator += 1
        # print(f"Now player {players[iterator]}'s turn")
        
        # to_board = players[iterator]
        # serialcomm.write(to_board.encode())


    cv2.imshow("Image", img)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break  

    i = "Pending"
    j = ""
    if draw_card == 1 and turn_used == 0:
        i = "shoot card"
        #time.sleep(0.2)
        turn_used = 1
        cards_left -= 1
    elif next_turn == 1:
        i = "next turn/"
        j = players[iterator]
        i += j
        #time.sleep(0.2)
        turn_used = 0
    else:
        i = "Pending"
        continue
    print(turn_used)
    serialcomm.write(i.encode())
    # serialcomm.write(j.encode())
    time.sleep(0.5)
    print(serialcomm.readline().decode('ascii'))

serialcomm.close()

cap.release()
cv2.destroyAllWindows()