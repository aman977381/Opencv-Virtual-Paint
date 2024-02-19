# Import libraries
import numpy as np
import cv2

# Capture video from webcame
frameWidth = 520
frameHeight = 480
cap = cv2.VideoCapture(0) # Type the adress of your webcame if you are using laptop then let it be 0
cap.set(3, frameWidth)
cap.set(4,frameHeight)
cap.set(10,100)

# Color Detection

myColor = [
            #[5,107,0,19,255,255], #Orange
           [90, 50, 50, 130, 255, 255], # Blue 
           [35, 55, 55, 80, 255, 255], # Green 
           #[20, 50, 50, 40, 255, 255] # Yellow
           ]
myColorValues = [
                #[0, 128, 255],    ## BGR
                 [255, 0, 0],
                 [0, 255, 0],
                 #[0, 255, 255]
                 ]
myPoints = [] # [x, y, colorId]


# Detecting colors
def findcolor(img,myColor,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoint = []
    for color in myColor:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask  = cv2.inRange(imgHSV,lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult, (x,y), 5, myColorValues[count], cv2.FILLED)

        if x!= 0 and y!=0:
            newPoint.append([x,y,count])
        count +=1
    
    return newPoint

        #cv2.imshow(str(color[0]), mask)
    #imgResult = cv2.bitwise_and(img, img, mask = mask)
        

# Bounding Box
def getContours(img):
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w = 0,0,0
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgResult, cnt, -1, (255,0,0),3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)

    return x+(w//2), y


# Lets draw on canvas
def drawOnCanvas (myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0],point[1]), 10, myColorValues[point[2]],cv2.FILLED)



while True:

    success, img = cap.read()
    imgResult = img.copy()
    newPoint = findcolor(img,myColor,myColorValues)

    if len(newPoint)!=0:
        for newP in newPoint:
            myPoints.append(newP)

    if len(myPoints)!= 0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break 