import cv2
import numpy as np

img = cv2.imread("1458306694.10.png",1)
gray = cv2.imread("1458306694.10.png",0)
_, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


# des = cv2.bitwise_not(gray)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
# des = cv2.erode(thresh,kernel,iterations = 1)
# des = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
# des = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
# des = cv2.erode(thresh,kernel,iterations = 1)
# des = cv2.dilate(thresh,kernel,iterations = 1)
# des = cv2.erode(des,kernel,iterations = 1)
# cv2.imshow('h',des)

# hier,contour,hier = cv2.findContours(des,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
# for cnt in contour:
	# cv2.drawContours(des,[cnt],0,255,-1)
# gray = cv2.bitwise_not(des)
# cv2.imwrite('img3.png',gray)


cv2.imshow('img',img)
cv2.imshow('gray',gray)
cv2.imshow('thresh',thresh)
cv2.imshow('des',des)
cv2.waitKey()