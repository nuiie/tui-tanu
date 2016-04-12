from tuilib import Tui
from boardlib import Board
from causallib import causalBox
from playerlib import GameCtrler
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
	if k & 0xFF == ord('q'): 	# press q for quit

		print "exit"
		return False
		
	elif k & 0xFF == ord('p'): 	# press p for plot detected tuis
		if tuis is not None:
			print "plot"
			plot(tuis).show()
		else:
			print "no tui detected"
			
	elif k & 0xFF == ord('s'): 	# press s for save detected tuis
		if tuis is not None:
			ts = time.time()
			for i,tui in zip( range(len(tuis)), tuis):
				cv2.imwrite('.\\image\\rawImg\\'+str(ts)+str(i)+'.png',tui.rawImg)
			print 'saved',len(tuis)
		else:
			print "no tui detected"
			
	elif k & 0xFF == ord('t'): 	# press t for save thresh 
		if tuis is not None:
			ts = time.time()
			for i,tui in zip( range(len(tuis)), tuis):
				cv2.imwrite('.\\image\\thresh\\'+str(ts)+str(i)+'.png',tui.thresh)
			print 'saved',len(tuis)
		else:
			print "no tui detected"
			
	elif k & 0xFF == ord('g'):  # press g for get all rawImg thresh and letter
		if tuis is not None:
			ts = time.time()
			for i,tui in zip( range(len(tuis)), tuis):
				cv2.imwrite('.\\image\\rawImg\\'+str(ts)+str(i)+'.png',tui.rawImg)
				cv2.imwrite('.\\image\\thresh\\'+str(ts)+str(i)+'.png',tui.thresh)
				cv2.imwrite('.\\image\\letter\\'+str(ts)+str(i)+'.png',tui.letter)
			print 'saved',len(tuis)
		else:
			print "no tui detected"
	
	elif k & 0xFF == ord(' '): 	# press spaecbar for end subround
		pass
					
	return True
	

	
def main():
	#camera setup
	cap = cv2.VideoCapture(1)
	print 'Video resolution: '+' x '.join(set_res(cap,1280,720))
	tuis = []
	hBox = causalBox(winSize = 10)
	vBox = causalBox(winSize = 10)
	ret = True
	clf = getClassifier()
	plyerName = ["John","Doe","Tommy","Emmanuel"]
	game = GameCtrler(plyerName)
	while ret:
		now = time.time() # get the time
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
			
			hTuiTmp = []
			vTuiTmp = []
			for tui in tuis: # latter + name
				tui.getLetter()
				if tui.letter.size == 0:
					print 'letter size 0'
				else:
					letterPercentage = float(np.count_nonzero(tui.letter))/tui.letter.size*100.0
					if  letterPercentage > 3.9: # if letter area is more than 3.9% of img
						tui.getHuMoment()
						tui.getTuiName(clf)
				# split h and v tuis for feed in causalbox
				if tui.position[0] == 'h':
					hTuiTmp.append((tui.position[1],tui.name))
				elif tui.position[0] == 'v':
					vTuiTmp.append((tui.position[1],tui.name))
				else: print "invalid h/v tui position"		
			
		
			hBox.feedIn(hTuiTmp) # feed causalbox
			vBox.feedIn(vTuiTmp)
			
			# choose v or h
			a = board.vertical.copy() if len(vBox.tuis) > len(hBox.tuis) else board.horizontal.copy()
			b = vBox.tuis if len(vBox.tuis) > len(hBox.tuis) else hBox.tuis
			
			game.setArea(a) #set player area
			
			
			
			for i in b:
				cv2.circle(a,i.position,np.round(board.size*210/14),(0,255,0),2) # draw the outer circle
				cv2.circle(a,i.position,2,(0,0,255),3) # draw the center of the circle
				if i.isLegit:
					cv2.putText(a, i.getVotedName()[0][0], i.position, cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),4) # write name on img
			cv2.namedWindow('a', cv2.WINDOW_NORMAL)
			cv2.imshow('a',a)

		else:
			print 'No circle in both hor and ver a4'
				
		# display
		cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
		cv2.imshow('thresh',board.thresh)
		cv2.namedWindow('boardDetect', cv2.WINDOW_NORMAL)
		cv2.imshow('boardDetect',board.boardDetect)
	
		# condition for exit
		# if len(tuis) > 0:
			# ret = stop(cv2.waitKey(1), tuis)
		# else:
			# ret = stop(cv2.waitKey(1))
		
		k = cv2.waitKey(1)
		if k & 0xFF == ord('q'): 	# press q for quit
			print "exit"
			return False
		elif k & 0xFF == ord(' '):  # end subround
			game.endSubRound(b)
			for p in game.players:
				print p.name, p.tuisSubRound, p.sumSubRoundScore
			print game.boardScore
		# time controller
		elapsed = time.time() - now  # how long was it running?
		if elapsed < 0.2:
			time.sleep(0.2-elapsed)       # sleep accordingly so the full iteration takes 1 second
		elapsed = time.time() - now  # how long was it running?
		print str(elapsed)+":",
	
	cv2.destroyAllWindows()
		
	
	return 0	

	
main()