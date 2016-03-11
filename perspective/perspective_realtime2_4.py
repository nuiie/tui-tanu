# this is for opencv 2.4.10

import cv2
import numpy as np
from matplotlib import pyplot as plt
import random


def Adaptive_Threshold(im,adaptiveWinSize=None):
	if adaptiveWinSize is None:
		adaptiveWinSize = 95
	th = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,adaptiveWinSize,2)
	return th

def fillContour(img,color):
	contour,hier = cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	screenCnt = None
	x,y,w,h = [0,0,0,0]
	verA4 = None
	horA4 = None
	contour = sorted(contour, key = cv2.contourArea, reverse = True)
	for c in contour:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		if len(approx) == 4:
			screenCnt = approx
			break
	if screenCnt is not None:
		verA4 = PerspecTrans(screenCnt,color,[210,297])
		horA4 = PerspecTrans(screenCnt,color,[297,210])
	cv2.drawContours(color, [screenCnt], -1, (0, 255, 0), 3)
	return color,verA4,horA4
	
	
def PerspecTrans(pnt1,color,wh):
	point = []
	w,h = wh
	for x in pnt1:
		point.append([x[0][0], x[0][1]])
	point1 = [point[0],point[3], point[1], point[2]]
	point1 = np.float32(point1)
	point2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
	M = cv2.getPerspectiveTransform(point1,point2)
	dst = cv2.warpPerspective(color,M,(w,h))
	return dst

	
def set_res(cap, x,y):
	cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, int(x))
	cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, int(y))
	return str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

def main():
	
	#camera setup
	cap = cv2.VideoCapture(0)
	print set_res(cap,1280,720)
	
	while True:
		
		# Capture frame-by-frame
		ret, img = cap.read()
		img = cv2.medianBlur(img,3)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		# th = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,3,2)
		ret2,th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		cv2.namedWindow('THRESH_OTSU', cv2.WINDOW_NORMAL)
		cv2.imshow('THRESH_OTSU',th2)
		th1,verA4,horA4 = fillContour(th2,img)
		
		cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
		cv2.imshow('Original',th1)
		if verA4 is not None and horA4 is not None:
			cv2.imshow('Vertical',verA4)
			cv2.imshow('Horizontal',horA4)
		
		"""
		"""
		# cv2.namedWindow('b', cv2.WINDOW_NORMAL)
		# cv2.imshow('b',img)
		k = cv2.waitKey(1)
		if k & 0xFF == ord('q'):
			break
		elif k & 0xFF == ord('c'):
			cv2.imwrite('verA4.png',verA4)
			cv2.imwrite('horA4.png',horA4)
			print 'image saved'
			
			
	
	return 0

main()	


# conner detection

		# gray = np.float32(gray)	
		# dst = cv2.cornerHarris(gray,2,3,0.04)
		# dst = cv2.dilate(dst,None)
		# img[dst>0.01*dst.max()]=[0,0,255]