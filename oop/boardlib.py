import cv2
import numpy as np

class Board:
	# class __doc__
	"Board class contains untransformed, transformed, vertical and horizontal board"
	
	# class enumerate
	both, vertical, horizontal = xrange(3)
	
	def __init__(self, rawImg):
	
		rawImg = cv2.medianBlur(rawImg,3)
		self.rawImg 			= rawImg
		self.gray				= cv2.cvtColor(rawImg,cv2.COLOR_BGR2GRAY)
		self.hsv				= cv2.cvtColor(rawImg,cv2.COLOR_BGR2HSV)
		_, self.thresh			= cv2.threshold(self.gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		self.boardDetect		= rawImg.copy()
		self.horizontal			= np.uint8(np.zeros((210, 297, 3)))
		self.vertical			= np.uint8(np.zeros((297, 210, 3)))
		self.boardCnt			= None
		self.size 				= 1
		self.horizontalCircles	= None
		self.verticalCircles  	= None
		self.horizontal2		= np.uint8(np.zeros((210, 297, 3)))
		self.vertical2			= np.uint8(np.zeros((297, 210, 3)))
	
	def getBoardCnt(self):
	
		# get all contours
		contours,hier = cv2.findContours(self.thresh.copy(),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted(contours, key = cv2.contourArea, reverse = True)
		
		# find biggest rectangle contour as board
		boardCnt = None
		for cnt in contours:
			peri = cv2.arcLength(cnt, True)
			approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
			if len(approx) == 4:
				boardCnt = approx
				break
				
		# draw board and archive contour
		cv2.drawContours(self.boardDetect, [boardCnt], -1, (0, 255, 0), 3)
		self.boardCnt = boardCnt
		
		
	def getA4(self, size=1):
	
		self.size = size
		self.getBoardCnt()
		
		# transform board to A4 size
		if self.boardCnt is not None:
			self.vertical 	= np.uint8(self.getPerspectiveTransform([210*size,297*size]))
			self.horizontal = np.uint8(self.getPerspectiveTransform([297*size,210*size]))
		else:
			print 'Board not found'
	
	
	def getPerspectiveTransform(self, wh):
	
		point = []
		w,h = wh
		for x in self.boardCnt:
			point.append([x[0][0], x[0][1]])
		point1 = [point[0],point[3], point[1], point[2]]
		point1 = np.float32(point1)
		point2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
		M = cv2.getPerspectiveTransform(point1,point2)
		dst = cv2.warpPerspective(self.rawImg.copy(),M,(w,h))
		return dst
	
	
	def getCircle(self):
		
		# calculate max min rad based on a4 size image
		shortSide = self.size*210
		minCalRad = np.round(shortSide/30)
		maxCalRad = np.round(shortSide/14)
		
		# find circle
		self.verticalCircles 	= cv2.HoughCircles( cv2.cvtColor(self.vertical,cv2.COLOR_BGR2GRAY) ,cv2.cv.CV_HOUGH_GRADIENT,1,minCalRad,param1=50,param2=30,minRadius=minCalRad,maxRadius=maxCalRad)
		self.horizontalCircles	= cv2.HoughCircles( cv2.cvtColor(self.horizontal,cv2.COLOR_BGR2GRAY) ,cv2.cv.CV_HOUGH_GRADIENT,1,minCalRad,param1=50,param2=30,minRadius=minCalRad,maxRadius=maxCalRad)
	

	def drawCircles(self):
	
		if self.verticalCircles is not None:
			self.vertical2 = self.vertical.copy()
			for i in self.verticalCircles[0,:]:
				
				# draw the outer circle
				cv2.circle(self.vertical2,(i[0],i[1]),i[2],(0,255,0),2)
				# draw the center of the circle
				cv2.circle(self.vertical2,(i[0],i[1]),2,(0,0,255),3)
							
		if self.horizontalCircles is not None:
			self.horizontal2 = self.horizontal.copy()
			for i in self.horizontalCircles[0,:]:
				
				# draw the outer circle
				cv2.circle(self.horizontal2,(i[0],i[1]),i[2],(0,255,0),2)
				# draw the center of the circle
				cv2.circle(self.horizontal2,(i[0],i[1]),2,(0,0,255),3)