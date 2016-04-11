from tuilib import Tui
from boardlib import Board
from causallib import causalBox
from matplotlib import pyplot as plt
import cv2
import time
import numpy as np
import cPickle
from sklearn.ensemble import RandomForestClassifier

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
			plt.title(tuis[i].name)
		else:	
			plt.title(str(i))
		plt.xticks([]),plt.yticks([])
	return plt

def getClassifier():
	with open('forest/forest02.pickle', 'rb') as f:
		clf = cPickle.load(f)
	return clf

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
			
	# press g for get all rawImg thresh and letter
	elif k & 0xFF == ord('g'):
		if tuis is not None:
			ts = time.time()
			for i,tui in zip( range(len(tuis)), tuis):
				cv2.imwrite('.\\image\\rawImg\\'+str(ts)+str(i)+'.png',tui.rawImg)
				cv2.imwrite('.\\image\\thresh\\'+str(ts)+str(i)+'.png',tui.thresh)
				cv2.imwrite('.\\image\\letter\\'+str(ts)+str(i)+'.png',tui.letter)
			print 'saved',len(tuis)
		else:
			print "no tui detected"
			
	# press o for print position
	if k & 0xFF == ord('o'):
		if tuis is not None:
			for tui in tuis:
				print tui.position
		else:
			print "No tui for display position"
		
	# default continue tui-tanu
	return True

def labelTui(board, tuis):
	# init font
	font = cv2.FONT_HERSHEY_SIMPLEX
	
	for tui in tuis:
		if tui.name is None: # check label
			print 'tui has no name'
		else:
			if tui.position[0] == 'v':
				cv2.putText(board.vertical2,tui.name,tui.position[1], font, 1,(255,0,0),4)
			elif tui.position[0] == 'h':
				cv2.putText(board.horizontal2,tui.name,tui.position[1], font, 1,(255,0,0),4)
			else:
				print 'invalid tui position:', tui
	return 0

def main():

	
	
	#camera setup
	cap = cv2.VideoCapture(1)
	print 'Video resolution: '+' x '.join(set_res(cap,1280,720))
	tuis = []
	hBox = causalBox(winSize = 10)
	vBox = causalBox(winSize = 10)
	ret = True
	clf = getClassifier()
	while ret:
		# time controller
		now = time.time() # get the time
		
		# get image
		ret, rawImg = cap.read()
		if ret is False:
			print "Error aquring image"
			break
		board = Board(rawImg)
		board.getA4(size = 4)
		board.getCircle()
		
		# setup causal Box
		lenNeighbor = np.round(board.size*210/14)
		vBox.setThresh(lenNeighbor)
		hBox.setThresh(lenNeighbor)
		
		# check if circles in A4
		if board.horizontalCircles is not None or board.verticalCircles is not None:
			board.drawCircles()
			tuis = board.getTuis()
			print len(tuis),'tuis found'
			
			
			hTuiTmp = []
			vTuiTmp = []
			for tui in tuis:
				# latter + name
				tui.getLetter()
				if tui.letter.size == 0:
					print 'letter size 0'
				else:
					letterPercentage = float(np.count_nonzero(tui.letter))/tui.letter.size*100.0
					if  letterPercentage > 3.9: # if letter area is more than 3.9% of img
						tui.getHuMoment()
						tui.getTuiName(clf)
					else:
						print 'too less letter area percentage:', letterPercentage
				
				# split h and v tuis for feed in box
				if tui.position[0] == 'h':
					hTuiTmp.append((tui.position[1],tui.name))
				elif tui.position[0] == 'v':
					vTuiTmp.append((tui.position[1],tui.name))
				else: print "invalid h/v tui position"
			
			# labelTui(board,tuis)
			
			
			
			hBox.feedIn(hTuiTmp)
			vBox.feedIn(vTuiTmp)
			print "hLegit:", len(hBox.tuis)
			print "vLegit:", len(vBox.tuis)
			
			a = board.horizontal.copy()
			for i in hBox.tuis:
				if i.isLegit:
					# draw the outer circle
					cv2.circle(a,i.position,np.round(board.size*210/14),(0,255,0),2)
					# draw the center of the circle
					cv2.circle(a,i.position,2,(0,0,255),3)
					# write name on img
					cv2.putText(a, i.getVotedName()[0][0], i.position, cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),4)
				else: 
					# draw the outer circle
					cv2.circle(a,i.position,np.round(board.size*210/14),(0,0,255),2)
					# draw the center of the circle
					cv2.circle(a,i.position,2,(0,0,255),3)
			cv2.namedWindow('a', cv2.WINDOW_NORMAL)
			cv2.imshow('a',a)

			
		else:
			print 'No circle in both hor and ver a4'
				
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
		
		# time controller
		elapsed = time.time() - now  # how long was it running?
		if elapsed < 0.2:
			time.sleep(0.2-elapsed)       # sleep accordingly so the full iteration takes 1 second
		elapsed = time.time() - now  # how long was it running?
		print str(elapsed)+":",
			
	cv2.destroyAllWindows()
		
	
	return 0	

	
main()