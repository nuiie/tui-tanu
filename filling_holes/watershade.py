import numpy as np
import cv2
from matplotlib import pyplot as plt
import math


def run_main():
	gray = cv2.imread("img3.png", cv2.IMREAD_GRAYSCALE)
	img = cv2.imread("img2.png")
	gray = cv2.bitwise_not(gray)

	# noise removal
	kernel = np.ones((3,3),np.uint8)
	opening = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel, iterations = 2)
	opening = cv2.medianBlur(opening,15)
	# sure background area
	sure_bg = cv2.dilate(opening,kernel,iterations=3)

	# Finding sure foreground area
	dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
	ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

	# Finding unknown region
	sure_fg = np.uint8(sure_fg)
	unknown = cv2.subtract(sure_bg,sure_fg)

	# # Marker labelling
	# ret, markers = cv2.connectedComponents(sure_fg)
	
	# # Add one to all labels so that sure background is not 0, but 1
	# markers = markers+1
	# print len(markers),markers[0]
	# cv2.imshow('m',markers[2])
	# # Now, mark the region of unknown with zero
	# markers[unknown==255] = 0
	# cv2.imshow('u',unknown)
	# cv2.imshow('b',sure_bg)
	# cv2.imshow('f',sure_fg)
	
	
	# markers = cv2.watershed(gray,markers)
	# gray[markers == -1] = [255,0,0]


	hierarchy,contours, hierarchy = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		# area = cv2.contourArea(cnt)/0.8
		# if area < 2000 or area > 4000:
			# continue

		# if len(cnt) < 5:
			# continue
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius*3.25)
		img = cv2.circle(img,center,radius,(0,255,0),2)

		# ellipse = cv2.fitEllipse(cnt)
		# print ellipse
		# cv2.ellipse(img, ellipse, (0,255,0), 2)
	print len(contours)
	cv2.imshow('final result', img)
	
	
	
	
	
	cv2.waitKey()
if __name__ == "__main__":
	run_main()