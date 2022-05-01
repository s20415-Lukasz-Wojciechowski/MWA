
import cv2
import argparse
import math

def parse_arguments():
    parser = argparse.ArgumentParser(description=('Plane'))
    parser.add_argument('-i','--input_video',type=str,required=True,help='video file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

video = cv2.VideoCapture(args.input_video)
if not video.isOpened():
    print("Can not open")
    exit();
flow=[]
treshhold = 50
while True:
    ret,frame = video.read()
    if frame is None:
        break;
    cv2.waitKey(1)
    frame = cv2.resize(frame, (1500,900))
    blur = cv2.GaussianBlur(frame, (11, 11), 1)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(gray, mask=None, maxCorners = 100,qualityLevel = 0.3, minDistance = 7, blockSize = 7)

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    p1, st, err = cv2.calcOpticalFlowPyrLK(gray, frame_gray, p0, None, winSize  = (15,15), maxLevel = 1,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    good_old = p0[st==1]
    good_new = p1[st==1]

    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        if len(flow) == 0:
            flow.append((int(a), int(b)))
        oldX = flow[-1][0]
        oldY = flow[-1][1]

        x = math.pow(int(a)-oldX,2)
        y = math.pow(int(b)-oldY,2)

        if(math.sqrt(x+y)<treshhold):
            flow.append( (int(a), int(b)))

    for i in flow:
        cv2.circle(frame, i, radius=2, color=(255, 255, 255), thickness=-1)

    cv2.imshow("plane", frame)