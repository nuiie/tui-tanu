# track imported image

import cv2
import numpy as np

#get image

img = cv2.imread('Screenshot.jpg')

#convert colorspace to HSV
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_red = np.array([167,50,50])
upper_red = np.array([187,255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(img2, lower_red, upper_red)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(img,img, mask= mask)

cv2.imshow('res',res)
cv2.imshow('mask',mask)
cv2.imshow('imgage',img)
cv2.imshow('imgage2',img2)
while(1):
	if cv2.waitKey(1) == ord('q'):
		break