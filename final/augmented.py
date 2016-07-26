from boardlib import Board
from tuilib import Tui
import numpy as np
import cv2
from scipy.spatial import distance as dist

class Augmented:

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
			
	def getObjp(self, board):
		j, i, _ = board.causalBoard.shape
		# i = i/20.0
		# j = j/20.0
		objp = np.float32([[0,0,0],[0,j,0],[i,j,0],[i,0,0]])
		objp[:,:2] = self.order_points(objp[:,:2]).reshape(-1,2)
		return objp
		
	def getAxis(self, position = (0,0)):
		i, j = position
		i = i/20.0
		j = j/20.0
		size = 0.3
		axis = np.float32([[i,j,0],[i,j+size,0],[i+size,j+size,0],[i+size,j,0],[i,j,-size],[i,j+size,-size],[i+size,j+size,-size],[i+size,j,-size]])
		return axis
		
	def getTuiBoundary(self, position, r):
		axis = np.float32([[0,0,0], [0,1,0], [1,1,0], [1,0,0]])
		i, j = position
		p1 = [i+r,j+r]
		p2 = [i+r,j-r]
		p3 = [i-r,j+r]
		p4 = [i-r,j-r]
		axis[:,:2] = self.order_points(np.float32([p1,p2,p3,p4])).reshape(-1,2)
		return axis
		
	def getBoardVecs(self, board):
		mtx, dist = self.loadCalib()
		objp = self.getObjp(board)
		imgp = np.float32(board.boardPos)
		_, rvecs, tvecs = cv2.solvePnP(objp, imgp, mtx, dist)
		return rvecs, tvecs
		
	def getTPts(self, t, board, rvecs, tvecs):
		rTui = np.round(board.size*210/12) # radius of tui
		mtx, dist = self.loadCalib()
		axis = self.getTuiBoundary(t.position, rTui)
		imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
		return imgpts
		
	def start(self, board, tuis):
		vecs = []
		bVecs, bTvecs = self.getBoardVecs(board)
		rvecs = None
		tvecs = None
		img = board.rawImg.copy()
		for t in tuis:
			imgpts = self.getTPts(t, board, bVecs, bTvecs)
			imgpts = np.int32(imgpts).reshape(-1,2)
			cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),3)
			
			rvecs, tvecs = self.passBackVecs(board.rawImg.copy(), imgpts)
			# ar, rvecs, tvecs = self.renderCube(mtx, dist, image, objp, axis, imgp)
			vecs.append([rvecs, tvecs, t.getVotedName()])
			
		# cv2.namedWindow('img', cv2.WINDOW_NORMAL)
		# cv2.imshow('img',img)
		return vecs
		
	def passBackVecs(self, image, points):		
		# load calibration data
		mtx, dist = self.loadCalib()
		
		# set up criteria, image, points and axis
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		imgp = np.array(self.order_points(points), dtype="float32")

		objp = np.array([[0.,0.,0.],[1.,0.,0.],
		[1.,1.,0.],[0.,1.,0.]], dtype="float32")  
		objp[:,:2] = self.order_points(objp[:,:2]).reshape(-1,2)

		# project 3D points to image plane
		cv2.cornerSubPix(gray,imgp,(11,11),(-1,-1),criteria)
		_, rvecs, tvecs = cv2.solvePnP(objp, imgp, mtx, dist)

		return rvecs, tvecs
	
	def loadCalib(self):
		with np.load('calibrateMtx.npz') as X:
			mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
		return mtx, dist
		
	def renderCube(self, mtx, dist, image, objp, axis, imgp):
		
		_, rvecs, tvecs = cv2.solvePnP(objp, imgp, mtx, dist)
		imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
		
		self.drawCube(image,imgpts)
		
		return image, rvecs, tvecs

	def drawCube(self, img, imgpts):
		imgpts = np.int32(imgpts).reshape(-1,2)

		# draw ground floor in green
		cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),3)

		# draw pillars in blue color
		for i,j in zip(range(4),range(4,8)):
			cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)

		# draw top layer in red color
		cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

		return img
		
	def markCorner(self, image,  rect):
		colors = ((0, 255, 255), (0, 0, 192), (0, 0, 192), (0, 0, 0))
		for ((x, y), color) in zip(rect, colors):
			cv2.circle(image, (int(x), int(y)), 5, color, -1)
		# return image