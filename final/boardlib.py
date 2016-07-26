import cv2
from scipy.spatial import distance as dist
import numpy as np
from tuilib import Tui

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
		self.hsvThresh			= None
		_, self.thresh			= cv2.threshold(self.gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		self.boardDetect		= rawImg.copy()
		self.horizontal			= np.uint8(np.zeros((210, 297, 3)))
		self.vertical			= np.uint8(np.zeros((297, 210, 3)))
		self.horMtx				= None
		self.verMtx				= None
		self.boardPos			= None
		self.size 				= 1
		self.horizontalCircles	= None
		self.verticalCircles  	= None
		self.horizontal2		= np.uint8(np.zeros((210, 297, 3)))
		self.vertical2			= np.uint8(np.zeros((297, 210, 3)))
		self.perspecMtx			= None
		self.causalBoard		= np.uint8(np.zeros((210, 297, 3)))
	
	def start(self, size = 1):
		self.size = size
		self.getBoardCnt()
		self.getA4()
		self.getCircle()
		self.drawCircles()
		return 0
	
	def getBoardCnt(self):
	
		# get all contours
		contours,hier = cv2.findContours(self.thresh.copy(),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
		boardCnt = None
		# find biggest rectangle contour as board
		for cnt in contours:
			peri = cv2.arcLength(cnt, True)
			approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
			if len(approx) == 4:
				boardCnt = approx
				break
		if boardCnt is None:
			print 'no rectangle in the secreen'
		else:
			cv2.drawContours(self.boardDetect, [boardCnt], -1, (0, 255, 0), 3)
			# chang format cnt -> [(xN,yN)*4]
			pts = []
			for pt in boardCnt:
				pts.append([pt[0][0],pt[0][1]])
			self.boardPos = self.order_points(np.array(pts))
			
	def getA4(self):
		if self.boardPos is not None:
			self.verMtx, self.vertical 	 = self.getPerspecTransform(210*self.size, 297*self.size)
			self.horMtx, self.horizontal = self.getPerspecTransform(297*self.size, 210*self.size)
		else:
			print "No board for Perspective transform"
		
	def order_points(self, pts):
		
		# sort the points based on their x-coordinates
		xSorted = pts[np.argsort(pts[:, 0]), :]

		# grab the left-most and right-most points from the sorted
		# x-roodinate points
		leftMost = xSorted[:2, :]
		rightMost = xSorted[2:, :]

		# now, sort the left-most coordinates according to their
		# y-coordinates so we can grab the top-left and bottom-left
		# points, respectively
		leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
		(tl, tr) = leftMost

		# now that we have the top-left coordinate, use it as an
		# anchor to calculate the Euclidean distance between the
		# top-left and right-most points; by the Pythagorean
		# theorem, the point with the largest distance will be
		# our bottom-right point
		D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
		(br, bl) = rightMost[np.argsort(D)[::-1], :]

		# return the coordinates in top-left, top-right,
		# bottom-right, and bottom-left order
		return np.array([tl, bl, br, tr], dtype="float32")

	def getPerspecTransform(self, i, j):
		
		dstPnt = np.float32([[0,0],[i-1,0],[i-1,j-1],[0,j-1]])
		M = cv2.getPerspectiveTransform(self.boardPos,dstPnt)
		dst = cv2.warpPerspective(self.rawImg.copy(),M,(i,j))
		return M,np.uint8(dst)
	
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
							
		elif self.horizontalCircles is not None:
			self.horizontal2 = self.horizontal.copy()
			for i in self.horizontalCircles[0,:]:
				
				# draw the outer circle
				cv2.circle(self.horizontal2,(i[0],i[1]),i[2],(0,255,0),2)
				# draw the center of the circle
				cv2.circle(self.horizontal2,(i[0],i[1]),2,(0,0,255),3)
		else:
			print "Both a4 is None Dont draw circle just yet"
				
	def getTuis(self, clf):

		tuiVer = []
		tuiHor = []
		
		# init position
		if self.verticalCircles is not None:
			for i in self.verticalCircles[0,:]:		
				center = (i[0],i[1])
				radius = self.size*297/19
				x1 = center[0]-radius
				y1 = center[1]-radius
				x2 = center[0]+radius
				y2 = center[1]+radius
				eachTui = Tui(self.vertical[y1:y2,x1:x2],['v',center])
				tuiVer.append(eachTui)
				
		if self.horizontalCircles is not None:
			for i in self.horizontalCircles[0,:]:
				center = (i[0],i[1])
				radius = self.size*297/19
				x1 = center[0]-radius
				y1 = center[1]-radius
				x2 = center[0]+radius
				y2 = center[1]+radius
				eachTui = Tui(self.horizontal[y1:y2,x1:x2],['h',center])
				tuiHor.append(eachTui)
		
		tuis = tuiHor+tuiVer
		# init type
		for tui in tuis: # latter + name
			tui.getLetter()
			if tui.letter.size == 0:
				print 'letter size 0'
			else:
				letterPercentage = float(np.count_nonzero(tui.letter))/tui.letter.size*100.0
				if  letterPercentage > 3.9: # if letter area is more than 3.9% of img
					tui.getHuMoment()
					tui.getTuiName(clf)
		return tuis

	def hasTui(self):
		return (self.verticalCircles is not None) or (self.horizontalCircles is not None)
	
	def isHor(self):
		if self.verticalCircles is None and self.horizontalCircles is None:
			return False
		elif self.verticalCircles is None and self.horizontalCircles is not None:
			return True
		elif self.verticalCircles is not None and self.horizontalCircles is not None:
			return len(self.verticalCircles[0,:]) < len(self.horizontalCircles[0,:])
	
	def isVer(self):
		if self.verticalCircles is None and self.horizontalCircles is None:
			return False
		elif self.verticalCircles is not None and self.horizontalCircles is None:
			return True
		elif self.verticalCircles is not None and self.horizontalCircles is not None:
			return len(self.verticalCircles[0,:]) > len(self.horizontalCircles[0,:])