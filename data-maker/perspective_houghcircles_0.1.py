# this is for opencv 2.4.10
import time
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
		size = 4
		verA4 = PerspecTrans(screenCnt,color,[210*size,297*size])
		horA4 = PerspecTrans(screenCnt,color,[297*size,210*size])
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

	
def findCircle(cimg):
	# img = cv2.medianBlur(img,1)
	# print id(cimg)
	img = cv2.cvtColor(cimg,cv2.COLOR_BGR2GRAY)
	# ret2,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# cv2.imshow('debug',img)
	minCalRad = np.round(len(img[0])/30)
	maxCalRad = np.round(len(img[0])/14)

	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,minCalRad,param1=50,param2=30,minRadius=minCalRad,maxRadius=maxCalRad)
	if circles is not None:
		circles = np.uint16(np.around(circles))
		
		for i in circles[0,:]:
			# draw the outer circle
			cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
			# draw the center of the circle
			cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
		return cimg,circles
	else:
		# print 'No circle detected'
		return None,None
	
def plot(images,titles=None):
	num_img = len(images)
	
	if titles is None:
		titles = range(len(images))
	row = int(num_img**0.5+1)
	for i in xrange(num_img):
		plt.subplot(row,row,i+1)
		plt.imshow(images[i])
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	return plt

	
def extractTui(img,circles):
	tui = []
	for i in circles[0,:]:		
		center = (i[0],i[1])
		radius = max(len(img[0]),len(img) )/19 #i[2]*1.2 # fixed size
		x1 = center[0]-radius
		y1 = center[1]-radius
		x2 = center[0]+radius
		y2 = center[1]+radius
		tui.append(img[y1:y2,x1:x2])
	return tui
	
def main():
	
	#camera setup
	cap = cv2.VideoCapture(0)
	print set_res(cap,1280,720)
	print "press p for plot, q for exit, c for save a4 img, s for save tui"
	while True:
		# innit
		eachTuiHor = []
		eachTuiVer = []
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
			# cv2.imshow('Vertical',verA4)
			# cv2.imshow('Horizontal',horA4)
			
			
			# np.copy for pass np array to function by value
			ansVer,circlesVer = findCircle(np.copy(verA4))
			ansHor,circlesHor = findCircle(np.copy(horA4))
			
			
			if ansVer is not None:
				cv2.imshow('circleVer',ansVer)
				# cv2.imshow('verA4',verA4)
				eachTuiVer = extractTui(verA4,circlesVer)
		
			
			if ansHor is not None:
				cv2.imshow('circleHor',ansHor)
				# cv2.imshow('horA4',horA4)
				eachTuiHor = extractTui(horA4,circlesHor)
				
				
		k = cv2.waitKey(1)
		if k & 0xFF == ord('q'):
			print "exit"
			break
		elif k & 0xFF == ord('c'):
			cv2.imwrite('verA4.png',verA4)
			cv2.imwrite('horA4.png',horA4)
			print 'image saved'
		elif k & 0xFF == ord('p'):
			print 'plot'
			plot(eachTuiHor).show()
			plot(eachTuiVer).show()
		elif k & 0xFF == ord('s'):
			ts = time.time()
			for name,tui in zip(range(len(eachTuiHor)),eachTuiHor):
				cv2.imwrite('.\\new\\horA4'+str(ts)+str(name)+'.png',tui)
			for name,tui in zip(range(len(eachTuiVer)),eachTuiVer):
				cv2.imwrite('.\\new\\verA4'+str(ts)+str(name)+'.png',tui)
			print 'saved',len(eachTuiVer),len(eachTuiHor)
	return 0

main()	