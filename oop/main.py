from tuilib import Tui
from boardlib import Board
from matplotlib import pyplot as plt
import cv2
import time
import numpy as np

def set_res(cap, x,y):
	cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, int(x))
	cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, int(y))
	return str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

	
def plot(tuis):
	num_tui = len(tuis)
		
	row = int(num_tui**0.5+1)
	for i in xrange(num_tui):
		plt.subplot(row,row,i+1)
		plt.imshow(tuis[i].letter)
		if tuis[i].name is not None:
			plt.title(tuis[i].rawImg)
		else:	
			plt.title(str(i))
		plt.xticks([]),plt.yticks([])
	return plt

	
def stop(k, tuis=None):
	
	# press q for quit
	if k & 0xFF == ord('q'):
		print "exit"
		return False
		
	# press p for plot detected tuis
	elif k & 0xFF == ord('p'):
		
		if tuis is not None:
			print "plot"
			plot(tuis).show()
		else:
			print "no tui detected"
			
	# press s for save detected tuis
	elif k & 0xFF == ord('s'):
		
		if tuis is not None:
			ts = time.time()
			for i,tui in zip( range(len(tuis)), tuis):
				cv2.imwrite('.\\image\\rawImg\\'+str(ts)+str(i)+'.png',tui.rawImg)
			print 'saved',len(tuis)
		else:
			print "no tui detected"
			
	# press t for save thresh 
	elif k & 0xFF == ord('t'):
		
		if tuis is not None:
			ts = time.time()
			for i,tui in zip( range(len(tuis)), tuis):
				cv2.imwrite('.\\image\\thresh\\'+str(ts)+str(i)+'.png',tui.thresh)
			print 'saved',len(tuis)
		else:
			print "no tui detected"
	# default continue tui-tanu
	return True

def main():

	#camera setup
	cap = cv2.VideoCapture(0)
	print 'Video resolution: '+' x '.join(set_res(cap,1280,720))
	
	ret = True
	while ret:
	
		# get image
		ret, rawImg = cap.read()
		if ret is False:
			print "Error aquring image"
			break
		board = Board(rawImg)
		
		board.getA4(size = 5)
		board.drawCircles()
		
		
		tuis = board.getTuis()
		n = len(tuis)
		if n > 0:
			for i,tui in zip(range(n),tuis):
				if tui.thresh is not None:
					pass
					# a = tui.getLetter()
				# cv2.imshow(str(i), tui.rawImg)
				# cv2.imshow(str(i)+"thresh", tui.thresh)
				# if a is not None:
				# cv2.imshow(str(i)+"letter", tui.letter)
					# print "found"
				# else:
					# print None
				
				
				
		# display
		cv2.namedWindow('rawImg', cv2.WINDOW_NORMAL)
		cv2.imshow('rawImg',board.rawImg)
		cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
		cv2.imshow('thresh',board.thresh)
		cv2.namedWindow('boardDetect', cv2.WINDOW_NORMAL)
		cv2.imshow('boardDetect',board.boardDetect)
		cv2.namedWindow('vertical', cv2.WINDOW_NORMAL)
		cv2.imshow('vertical',board.vertical)
		cv2.namedWindow('horizontal', cv2.WINDOW_NORMAL)
		cv2.imshow('horizontal',board.horizontal)
		cv2.namedWindow('vertical2', cv2.WINDOW_NORMAL)
		cv2.imshow('vertical2',board.vertical2)
		cv2.namedWindow('horizontal2', cv2.WINDOW_NORMAL)
		cv2.imshow('horizontal2',board.horizontal2)
	
		# condition for exit
		if len(tuis) > 0:
			ret = stop(cv2.waitKey(1), tuis)
		else:
			ret = stop(cv2.waitKey(1))
	cv2.destroyAllWindows()
		
	
	return 0	
		
		
		
		
		
main()