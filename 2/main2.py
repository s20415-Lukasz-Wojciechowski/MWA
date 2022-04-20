#Project created by Lukasz Wojciechowski
import sys

import cv2
import argparse
import numpy as np
import math

def parse_arguments():
    print("Calculating...")

link = "./tray6.jpg"
if __name__ == '__main__':
    parse_arguments()
img = cv2.imread(link)
img2 = cv2.imread(link,0)
img3 = cv2.medianBlur(img2,5)


if img is None:
    exit("can not open");


#Tray
edges = cv2.Canny(img2,180,300)
lines = cv2.HoughLinesP(edges,rho=1.1,theta=1.1*np.pi/180,threshold=70,minLineLength=10,maxLineGap=30)
[xmin ,ymin,xmax ,ymax ] = lines[0][0]
for i in lines:
    x1,y1,x2,y2 = i[0]

    #xmin
    if x1<xmin:
        xmin = x1
    if x2<xmin:
        xmin = x2
    #xmax
    if x1>xmax:
        xmax = x1
    if x2>xmax:
        xmax = x2

    #ymin
    if y1<ymin:
        ymin = y1
    if y2<xmin:
        ymin = y2
    #ymax
    if y1>ymax:
        ymax = y1
    if y2>ymax:
        ymax = y2
#Circles
total = 0
coinsIn = 0
circles = cv2.HoughCircles(img3, cv2.HOUGH_GRADIENT, 1.8, 40,100, param1=120,param2=55,minRadius=20,maxRadius=100)
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        cv2.circle(img, (x, y), r, (0, 255, 0), 4)
        total +=1
        if xmin<=x and xmax>=x:
            if ymin<=y and ymax>=y:
                coinsIn +=1

cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(240,204,221),6)
cv2.putText(img,"Total coins:"+str(total),(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA,False)
cv2.putText(img,"Coins in:"+str(coinsIn),(10,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA,False)
cv2.putText(img,"Coins out:"+str(total-coinsIn),(10,150),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv2.LINE_AA,False)
cv2.imshow("output", img)
cv2.waitKey(10000);
cv2.destroyAllWindows()