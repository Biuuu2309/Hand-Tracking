import cv2  
import time
import os
import sys

import cvzone.SerialModule
import HandTrackingModulee as htm  
import cvzone

wCam, hCam = 1280, 720
cap = cv2.VideoCapture(0)  
if not cap.isOpened(): 
    print("Error: Camera not accessible.")
    exit()

cap.set(3, wCam)
cap.set(4, hCam)

folderpath = ""
pTime = 0
detector = htm.handDetector(detectionCon=0.75)
mySerial = cvzone.SerialModule.SerialObject("COM3", 9600, 1)
tipIds = [4, 8, 12, 16, 20]

dicthand = {
    (1, 0, 0, 0, 0): "/1.png",(0, 1, 0, 0, 0): "/2.png",(0, 0, 1, 0, 0): "/3.png",(0, 0, 0, 1, 0): "/4.png",(0, 0, 0, 0, 1): "/5.png",
    (1, 1, 0, 0, 0): "/6.png",(1, 0, 1, 0, 0): "/7.png",(1, 0, 0, 1, 0): "/8.png",(1, 0, 0, 0, 1): "/9.png",(0, 1, 1, 0, 0): "/10.png",
    (0, 1, 0, 1, 0): "/11.png",(0, 1, 0, 0, 1): "/12.png",(0, 0, 1, 1, 0): "/13.png",(0, 0, 1, 0, 1): "/14.png",(0, 0, 0, 1, 1): "/15.png",
    (1, 1, 1, 0, 0): "/16.png",(1, 1, 0, 1, 0): "/17.png",(1, 1, 0, 0, 1): "/18.png",(1, 0, 1, 1, 0): "/19.png",(1, 0, 1, 0, 1): "/20.png",
    (0, 1, 1, 1, 0): "/21.png",(0, 1, 1, 0, 1): "/22.png",(0, 1, 0, 1, 1): "/23.png",(0, 0, 1, 1, 1): "/24.png",(1, 0, 0, 1, 1): "/25.png",
    (1, 1, 1, 1, 0): "/26.png",(1, 1, 1, 0, 1): "/27.png",(1, 1, 0, 1, 1): "/28.png",(1, 0, 1, 1, 1): "/29.png",(0, 1, 1, 1, 1): "/30.png",
    (1, 1, 1, 1, 1): "/31.png",(0, 0, 0, 0, 0): "/32.png"
}

while True:
    success, img = cap.read()
    if not success: 
        print("Error: Frame not captured.")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        finger = []
        #Right
        if (lmList[tipIds[0] - 3][1] > lmList[tipIds[0] - 4][1] and lmList[tipIds[4] - 3][2] < lmList[tipIds[0] - 4][2]) or ((lmList[tipIds[0] - 2][2] < lmList[tipIds[1] - 3][2]) and (lmList[tipIds[0] - 4][1] > lmList[tipIds[1] - 3][1])):
            #>90-left
            if lmList[tipIds[4] - 3][2] >= lmList[tipIds[0] - 4][2]:
                #
                if lmList[tipIds[0]][2] > lmList[tipIds[0] - 1][2]:
                    finger.append(0)
                else:
                    finger.append(1)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image right over -90"
                for id in range(1, 5):
                    if lmList[tipIds[id]][1] > lmList[tipIds[id] - 2][1]:
                        finger.append(0)
                    else:
                        finger.append(1)
            #>90-right
            elif lmList[tipIds[1] - 3][2] >= lmList[tipIds[0] - 4][2]:
                #
                if lmList[tipIds[0] - 1][2] > lmList[tipIds[0]][2]:
                    finger.append(0)
                else:
                    finger.append(1)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image right over 90"
                for id in range(1, 5):
                    if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]:
                        finger.append(0)
                    else:
                        finger.append(1)
            #0-90-right
            elif lmList[tipIds[4] - 3][1] > lmList[tipIds[0] - 4][1]:
                #
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  
                    if lmList[tipIds[1] - 3][1] > lmList[tipIds[0]][1]:
                        finger.append(0)
                    else:
                        finger.append(1)  
                else:
                    finger.append(0)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image right 90"
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        finger.append(1)
                    else:
                        finger.append(0)
                #
            #0-90-left
            elif lmList[tipIds[1] - 3][1] < lmList[tipIds[0] - 4][1]:
                #
                if lmList[tipIds[0]][2] > lmList[tipIds[0] - 1][2]:
                    finger.append(0)
                else: 
                    finger.append(1)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image right -90"
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        finger.append(1)
                    else:
                        finger.append(0)
            else:
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  
                    finger.append(1)  
                else:
                    finger.append(0)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image right 0"
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        finger.append(1)
                    else:
                        finger.append(0)
        #Left
        else:
            
            #>90-right
            if lmList[tipIds[4] - 3][2] > lmList[tipIds[0] - 4][2]:
                #
                if lmList[tipIds[0]][2] > lmList[tipIds[0] - 1][2]:
                    finger.append(0)
                else:
                    finger.append(1)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image left over 90"
                for id in range(1, 5):
                    if lmList[tipIds[id]][1] > lmList[tipIds[id] - 2][1]:
                        finger.append(1)
                    else:
                        finger.append(0)
            #>90-left
            elif lmList[tipIds[1] - 3][2] > lmList[tipIds[0] - 4][2]:
                #
                if lmList[tipIds[0]][2] < lmList[tipIds[0] - 1][2]:
                    finger.append(0)
                else:
                    finger.append(1)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image left over -90"
                for id in range(1, 5):
                    if lmList[tipIds[id]][1] > lmList[tipIds[id] - 2][1]:
                        finger.append(0)
                    else:
                        finger.append(1)
            #0-90-right
            elif lmList[tipIds[1] - 3][1] > lmList[tipIds[0] - 4][1]:
                #
                if lmList[tipIds[1] - 3][2] < lmList[tipIds[0]][2]:
                    finger.append(0)
                else:
                    finger.append(1)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image left 90"
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        finger.append(1)
                    else:
                        finger.append(0)
            #0-90-left
            elif lmList[tipIds[4] - 3][1] < lmList[tipIds[0] - 4][1]:
                #
                if lmList[tipIds[0]][2] < lmList[tipIds[0] - 1][2]:
                    finger.append(0)
                else: 
                    finger.append(1)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image left -90"
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        finger.append(1)
                    else:
                        finger.append(0)
            else:
                if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  
                    finger.append(1)  
                else:
                    finger.append(0)  
                folderpath = "Python Project/Hand-Tracking/Image rotate/Image left 0"
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        finger.append(1)
                    else:
                        finger.append(0)
                
        print(finger)
        mySerial.sendData(finger)
        finger_tuple = tuple(finger)  

        if finger_tuple in dicthand:
            image_path = folderpath + dicthand[finger_tuple]
            overlay_img = cv2.imread(image_path)

            if overlay_img is not None:
                h, w, c = overlay_img.shape
                img[0:h, 0:w] = overlay_img
                cv2.rectangle(img, (0, 128), (128, 256), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(finger.count(1)), (18, 245), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 10)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (950, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()
