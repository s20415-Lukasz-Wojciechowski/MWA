#Project created by Lukasz Wojciechowski
import cv2
import argparse
import numpy as np
import math

def parse_arguments():
    parser = argparse.ArgumentParser(description=('RBG'))
    parser.add_argument('-i','--input_video',type=str,required=True,help='video file')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

video = cv2.VideoCapture(args.input_video)
if not video.isOpened():
    print("Can not open")
    exit();

while True:
    ret,frame = video.read()
    if frame is None:
        break;
    cv2.waitKey(1)
    #bluring removes noises
    blurred_frame  = cv2.GaussianBlur(frame,(25,25),0)
    imgHSV = cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2HSV)

    low_red = np.array([141, 135, 64])
    high_red = np.array([199, 255, 255])
    #masks
    mask1 = cv2.inRange(imgHSV, low_red, high_red)
    karnel = np.ones((5,5),np.uint8)
    mask2 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,karnel)
    mask3 = cv2.morphologyEx(mask2,cv2.MORPH_CLOSE, karnel)
    red = cv2.bitwise_and(frame, frame, mask=mask3)

    contours, orient = cv2.findContours(mask3, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE )
    #find the biggest red area
    maxArea = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area>maxArea:
            maxContour = i;
            moment=cv2.moments(i)
            maxArea = area
    #center
    cX = int(moment["m10"] / moment["m00"])
    cY = int(moment["m01"] / moment["m00"])
    radius = math.ceil(math.sqrt(maxArea/math.pi))

    #mark a red object
    cv2.circle(red,(cX,cY),radius,(255,255,255),3)
    cv2.circle(frame,(cX,cY),radius,(255,255,255),3)

    #size of the window
    height = frame.shape[0]
    width = frame.shape[1]
    #Points from rectangle
    (size_h_min,size_w_min) = (height-100,width//4)
    (size_h_max,size_w_max) = (height-50,3*width//4)

    #deviation from center in scale (limited by the rectangle)
    follow = cX*(size_w_max-size_w_min)//width+width//4

    #dot follows a position of the red object - shows a deviation from the center
    cv2.rectangle(frame,(size_w_min, size_h_min),(size_w_max, size_h_max),(255,255,255),4)
    cv2.circle(frame,(follow,size_h_min+25),25,(0,255,0),-1)
    #display
    cv2.imshow("red",red)
    cv2.imshow('Frame',frame)