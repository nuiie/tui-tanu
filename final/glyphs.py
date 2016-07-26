from augmented import Augmented
import cPickle
from webcam import Webcam
import cv2
from boardlib import Board
from causallib import causalBox
import numpy as np
from playerlib import GameCtrler

def display(board):
	# cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
	# cv2.imshow('thresh',board.thresh)
	# cv2.namedWindow('a', cv2.WINDOW_NORMAL)
	# cv2.imshow('a',board.causalBoard)
	cv2.namedWindow('boardDetect', cv2.WINDOW_NORMAL)
	cv2.imshow('boardDetect',board.boardDetect)
	# cv2.imshow('hor',board.horizontal2)
	# cv2.imshow('ver',board.vertical2)
	# cv2.waitKey(100)
	
def getClassifier():
	with open('forest/forest02.pickle', 'rb') as f:
		clf = cPickle.load(f)
	return clf

def causalOutput(board, causalTuis):
	#causal output
	for i in causalTuis:
		cv2.circle(board.causalBoard ,i.position,np.round(board.size*210/14),(0,255,0),2) # draw the outer circle
		cv2.circle(board.causalBoard ,i.position,2,(0,0,255),3) # draw the center of the circle
		if i.isLegit:
			cv2.putText(board.causalBoard, i.getVotedName(), i.position, cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),4) # write name on img

def feedCausal(board, tuis, hBox, vBox):
	# setup causal Box
	lenNeighbor = np.round(board.size*210/14)
	vBox.setThresh(lenNeighbor)
	hBox.setThresh(lenNeighbor)
	
	# split h and v tuis for feed in causalbox
	hTuiTmp = []
	vTuiTmp = []
	for tui in tuis:
		if tui.position[0] == 'h':
			hTuiTmp.append((tui.position[1],tui.name))
		elif tui.position[0] == 'v':
			vTuiTmp.append((tui.position[1],tui.name))
			
	# feed causalbox
	hBox.feedIn(hTuiTmp) 
	vBox.feedIn(vTuiTmp)
	
	# choose v or h
	causalBoard = board.vertical.copy() if len(vBox.tuis) > len(hBox.tuis) else board.horizontal.copy()
	causalTuis = vBox.tuis[:] if len(vBox.tuis) > len(hBox.tuis) else hBox.tuis[:]
			
	return causalBoard, causalTuis
	
def detect_glyph(image, hBox, vBox, game):
	
	augmented = Augmented()
	board = Board(image)
	board.start(size = 4)
	if board.hasTui():
		tuis = board.getTuis(getClassifier())
		board.causalBoard, causalTuis = feedCausal(board, tuis, hBox, vBox)
		causalOutput(board, causalTuis)
		game.setArea(board.causalBoard)
		display(board)
		
		cv2.namedWindow('score', cv2.WINDOW_NORMAL)
		cv2.imshow('score', game.getScoreBoard())
		if cv2.waitKey(1) & 0xFF == ord(' '):  # end subround
			game.endSubRound(causalTuis[:])
		return augmented.start(board, causalTuis)
	else:
		display(board)
		if cv2.waitKey(1) & 0xFF == ord(' '):  # end subround
			self.game.endSubRound(causalTuis[:])
		return []
		
# webcam = Webcam()
# webcam.start()
# while True:
	# detect_glyph(webcam.get_current_frame())
	