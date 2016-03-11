import numpy as np
import numpy
import cv2
from matplotlib import pyplot as plt
import sys


def medBlur(im,blurWinSize=None):
	if blurWinSize is None:
		blurWinSize = 9
	blur = cv2.medianBlur(im,blurWinSize)
	return blur

	

def run_main():

	horA4 = cv2.imread("horA4.png",0)
	verA4 = cv2.imread("verA4.png",0)

	horA4 = medBlur(horA4,3)
	# verA4 = medBlur(verA4,3)
	
	circles = cv2.HoughCircles(horA4,cv2.cv.CV_HOUGH_GRADIENT,1.2,1)#,minRadius=12,maxRadius=13)
	
	
	if circles is not None:
		for i in circles[0,:]:
			# draw the outer circle
			cv2.circle(horA4,(i[0],i[1]),i[2],(0,255,0),2)
			# draw the center of the circle
			cv2.circle(horA4,(i[0],i[1]),2,(0,0,255),3)

		# cv2.imshow('detected circles',horA4)
		
		# horA4 = cv2.imread("horA4.png", cv2.IMREAD_GRAYSCALE)
	else:
		print "None circle"
	cv2.namedWindow('hor', cv2.WINDOW_NORMAL)
	cv2.imshow('hor',horA4)
	cv2.namedWindow('ver', cv2.WINDOW_NORMAL)
	cv2.imshow('ver',verA4)
	
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
if __name__ == "__main__":
	run_main()