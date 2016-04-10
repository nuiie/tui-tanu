from playerlib import GameCtrler
from tuilib import Tui
import numpy as np

def initTest(arg1, arg2):
	print "init test"
	board = ScoreBoard(arg1,arg2)
	for plyer in board.players:
		print plyer.name, plyer.position
	
	
#__innit___
arg1 = ["a","b","c","d"]
arg2 = [[(0,0),(5,5)], [(0,6),(5,10)], [(6,0),(10,5)], [(6,6),(10,10)]]
initTest(arg1,arg2)


def holderTest(arg1, arg2):
	print "holder test"
	board = ScoreBoard(arg1,arg2)
	img = np.zeros([100,100,3],dtype=np.uint8)
	a = [img]*8
	b = [ ('v',point) for point in [(1,1),(7,7),(8,3),(3,7)]*2 ]
	tuis = [Tui(img, position) for img, position in zip(a,b)]
	print "	Tui pos"
	for x in tuis:
		print x.position
	print " holder"
	board.findHolder(tuis)
	for plyer in board.players:
		print plyer.name, len(plyer.tuisRound)
	
holderTest(arg1, arg2)