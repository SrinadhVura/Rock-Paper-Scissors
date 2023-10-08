import cv2
import numpy as np
import screeninfo
import random
import HTrack as ht
import time
import math
"""
ROCK 0
PAPER 1
SCISSORS 2
"""

def playerTurn(d1,d2):
    if d1<90 and d2<90:
        return 0
    elif d1>115 and d2<90:
        return 2
    else:
        return 1

def computerTurn():
    return random.randint(0, 2)


rock=cv2.imread("S://NewGen//Rock_Paper_Scissors//images//Rock.png")
paper=cv2.imread("S://NewGen//Rock_Paper_Scissors//images//Paper.png")
scissors=cv2.imread("S://NewGen//Rock_Paper_Scissors//images//Scissors.png")
capture=cv2.VideoCapture(0)
capture.set(3,640)
capture.set(4,480)
detect=ht.handDetector(maxHands=1)
counter=0
startflag=False
stateflag=False
cscore,pscore=0,0
print("ROCK 0\nPAPER 1\nSCISSORS 2\n")
print("p c\n")

while True:
    _,img=capture.read()
    bg=cv2.imread("S://NewGen//Rock_Paper_Scissors//images//BG.jpg")
    cv2.imshow("Me",img)
    cv2.putText(bg,str(int(cscore)),(155,143),cv2.FONT_HERSHEY_COMPLEX,3,(0,42,255),4)
    cv2.putText(bg,str(int(pscore)),(813,143),cv2.FONT_HERSHEY_COMPLEX,3,(42,255,0),4)

    scaleimg=cv2.resize(img,(0,0),None,0.550,.55)
    scaleimg=scaleimg[:,69:322]
    handimg=detect.drawHands(scaleimg)
    found,lmarks=detect.getPositions(scaleimg)
    if startflag:
    #mid_tip and wrist distance
        if not stateflag:
            counter=time.time()-sTime
            cv2.putText(bg,str(int(counter)),(506,286),cv2.FONT_HERSHEY_PLAIN,5,(0,191,230),4)
            if counter>3:
                stateflag=True
                counter=0
                if found:
                    x1,y1=lmarks[0][1],lmarks[0][2]
                    x2,y2=lmarks[12][1],lmarks[12][2]
                    x3,y3=lmarks[16][1],lmarks[16][2]
                    d1=math.dist([x1,y1], [x2,y2])
                    d2=math.dist([x1,y1],[x3,y3])
                    pt=playerTurn(d1, d2)
                    ct=computerTurn()
                    if ct==0:
                        bg[170:434,63:316]=rock
                    elif ct==1:
                        bg[170:434,63:316]=paper
                    else :
                        bg[170:434,63:316]=scissors
                    if (pt==0 and ct==2) or (pt==1 and ct ==0) or (pt==2 and ct==1):
                        pscore+=1
                    if (ct==0 and pt==2) or (ct==1 and pt ==0) or (ct==2 and pt==1):
                        cscore+=1
                    print(pt,ct)
    # bg[170:434,63:316]=rock
    bg[170:434,702:955]=handimg
    if stateflag:
        if ct==0:
            bg[170:434,63:316]=rock
        elif ct==1:
            bg[170:434,63:316]=paper
        else :
            bg[170:434,63:316]=scissors 
    cv2.putText(bg,str(int(cscore)),(155,143),cv2.FONT_HERSHEY_COMPLEX,3,(0,42,255),4)
    cv2.putText(bg,str(int(pscore)),(813,143),cv2.FONT_HERSHEY_COMPLEX,3,(42,255,0),4)      
    cv2.imshow("BG",bg)
    # cv2.imshow("img",scaleimg)
    stkey=cv2.waitKey(1)
    if stkey==ord('s'):
        startflag=True
        sTime=time.time()
        stateflag=False
