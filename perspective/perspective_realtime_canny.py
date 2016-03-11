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
	img2,contour,hier = cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contour:
		cv2.drawContours(img,[cnt],0,255,-1)
	return img
	
def main():
	cap = cv2.VideoCapture(0)
	while True:
		
	
		# Capture frame-by-frame
		ret, img = cap.read()
		img = cv2.medianBlur(img,3)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		edged = cv2.Canny(gray, 30, 200)
		img2,cnts,hier = cv2.findContours(edged,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
		cnts = sorted(cnts, key = cv2.contourArea)
		screenCnt = None
		for c in cnts:
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)
			if len(approx) == 4:
				screenCnt = approx
				break
		cv2.drawContours(img, [screenCnt], -1, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), 3)
		cv2.namedWindow('a', cv2.WINDOW_NORMAL)
		cv2.imshow('a',img)
		
		k = cv2.waitKey(1)
		if k & 0xFF == ord('q'):
			break
	
	return 0

main()	


# conner detection

		# gray = np.float32(gray)	
		# dst = cv2.cornerHarris(gray,2,3,0.04)
		# dst = cv2.dilate(dst,None)
		# img[dst>0.01*dst.max()]=[0,0,255]