import time
import os

import cv2
import mediapipe as mp

import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# folderPath = "FingerImages"
# myList = os.listdir(folderPath)
# # print(myList)
# overlayList = []
# for imPath in myList:
#     image = cv2.imread(f"{folderPath}/{imPath}")
#     overlayList.append(image)
# # print(len(overlayList))

pTime = 0
tipIds = [4, 8, 12, 16, 20]
timeout = time.time() + 3
detector = htm.handDetector(detectionConf=0.75)
time_count = 0
current_finger = 99
previous_finger = 0
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
        # * other 4 fingers
        for idx in range(1, 5):
            if lmList[tipIds[idx]][2] < lmList[tipIds[idx] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)

        count = 0

        for i in fingers:
            if i == 1:
                count += 1

        # h, w, c = overlayList[count - 1].shape
        # img[0:w, 0:h] = overlayList[count - 1]

        if count != 0:
            print(f"The number of players is {count}")
            angle_per_player = 360 / count
            #print(angle_per_player)
            current_finger = count

        if count != 1:
            cv2.putText(img, f"{count} fingers", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        else:
            cv2.putText(img, "1 finger", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    #print(current_finger)
    #print(previous_finger)
    if current_finger == previous_finger:
        time_count += 1
    else: time_count = 0
    #print(time_count)

    cv2.putText(img, f"FPS: {int(fps)}", (450, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q") or (time_count == 50 and current_finger != 99): #or time.time() > timeout:
        break

print(count)
cap.release()
cv2.destroyAllWindows()
