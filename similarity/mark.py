import cv2
import numpy as np

img = cv2.imread('a.png')
gray = cv2.imread('a.png',0)

contours,hierarchy = cv2.findContours(np.copy(gray),2,1)
contours = sorted(contours, key = cv2.contourArea, reverse = True)
cnt = contours[0]
cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
hull = cv2.convexHull(cnt, returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)


for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img,start,end,[0,255,0],2)
    cv2.circle(img,far,5,[0,0,255],-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()