import cv2
import numpy as np

gray = cv2.imread("img2.png", cv2.IMREAD_GRAYSCALE)
des = cv2.bitwise_not(gray)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
des = cv2.erode(des,kernel,iterations = 1)
# des = cv2.morphologyEx(des, cv2.MORPH_CLOSE, kernel)
des = cv2.morphologyEx(des, cv2.MORPH_OPEN, kernel)
# des = cv2.erode(des,kernel,iterations = 2)
# des = cv2.dilate(des,kernel,iterations = 1)
des = cv2.erode(des,kernel,iterations = 1)
cv2.imshow('h',des)

hier,contour,hier = cv2.findContours(des,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
for cnt in contour:
	cv2.drawContours(des,[cnt],0,255,-1)
gray = cv2.bitwise_not(des)
cv2.imshow('gray',gray)
cv2.imwrite('img3.png',gray)

cv2.waitKey()