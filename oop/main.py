from tuilib import Tui
from boardlib import Board
import cv2
import numpy as np

def set_res(cap, x,y):
	cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, int(x))
	cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, int(y))
	return str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))


def main():
	
	#camera setup
	cap = cv2.VideoCapture(0)
	print 'Video resolution: '+' x '.join(set_res(cap,1280,720))
	
	
	while True:
		
		# get image
		ret, rawImg = cap.read()
		if ret is False:
			print "Error aquring image"
			break
		board = Board(rawImg)
		
		
		# board.getBoardCnt(Board.both)
		board.getA4(size = 1)
		board.getCircle()
		
		board.drawCircles()
		
		# display
		cv2.namedWindow('rawImg', cv2.WINDOW_NORMAL)
		cv2.imshow('rawImg',board.rawImg)
		cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
		cv2.imshow('thresh',board.thresh)
		cv2.namedWindow('boardDetect', cv2.WINDOW_NORMAL)
		cv2.imshow('boardDetect',board.boardDetect)
		# cv2.namedWindow('vertical', cv2.WINDOW_NORMAL)
		cv2.imshow('vertical',board.vertical2)
		# cv2.namedWindow('horizontal', cv2.WINDOW_NORMAL)
		cv2.imshow('horizontal',board.horizontal2)
		k = cv2.waitKey(1)
		if k & 0xFF == ord('q'):
			print "exit"
			break
	
main()