
import cv2
import numpy as np

if __name__ == '__main__':
    print("Running")
resizeHeight = 540
resizeWidth = 960
photo = "./saw1.jpg"
img = cv2.imread(photo)
img = cv2.resize(img,(resizeWidth,resizeHeight))
if img is None:
    print("ERROR")
#gray
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
dst = np.float32(gray)
hr = cv2.cornerHarris(dst,2,3,0.04)
img[hr>0.01*hr.max()] == [255,0,0]

corr = cv2.goodFeaturesToTrack(gray,125,0.01,1)
corr = np.int0(corr)

for i in corr:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)
#matching
img2 = cv2.imread("saw3.jpg")
img2 = cv2.resize(img2,(resizeWidth,resizeHeight))
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create()
p1,d1= orb.detectAndCompute(gray,None)
p2,d2= orb.detectAndCompute(gray2,None)

b = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
match = b.match(d1,d2)
match = sorted(match,key= lambda x:x.distance)

result = cv2.drawMatches(img,p1,img2,p2,match[:15],None,flags=2)
cv2.imshow("Matches",result)
cv2.imshow("Photo",img)
#video
video = cv2.VideoCapture('sawmovie.mp4')
while True:
    ret,frame = video.read();
    if frame is None:
        exit();
    cv2.waitKey(100)
    frame = cv2.resize(frame, (resizeWidth, resizeHeight))
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame2 =cv2.GaussianBlur(frame2, (5, 5), 0)
    orb = cv2.ORB_create()
    p3, d3 = orb.detectAndCompute(frame2, None)

    bfMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    match = b.match(d1, d3)
    match = sorted(match, key=lambda x: x.distance)

    result2 = cv2.drawMatches(img, p1, frame, p3, match[:3], None, flags=2)
    cv2.imshow("videoMatcher",result2)

