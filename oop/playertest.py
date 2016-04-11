from playerlib import GameCtrler
from playerlib import ScoreBoard
from playerlib import Player
from tuilib import TuiLegit
import numpy as np

def tuiInit(pos, name):
	winsize = 5
	print "TuiLigits"
	tuis = [TuiLegit(a,winsize,c) for a,c in zip(pos, name)]
	for x in tuis:
		x.votedName = x.name[0]
		x.getScore()
		print x.position, x.votedName, x.score
	print "return tuisLegits"
	print
	return tuis

tuiPos 	= [[0,0], [0,6],[3,8], [6,0],[8,5],[10,3], [6,10],[7,9],[8,7],[9,8]]
tuiName = ["R Horse", "B Phao", "B Phao", 'R T', "R Fly", 'R Ele', "B juk", "B juk", "B juk", "B juk"]
tuis = tuiInit(tuiPos,tuiName)

def gameInit(plyName,plyPos):
	print "Gmae init"
	game = GameCtrler(plyName, plyPos)
	for x in game.players:
		print x.name, x.area
	print "return game"
	print
	return game

	
plyName = ["a", "b", "c", "d"]
plyArea	= [[(0,0),(5,5)], [(0,6),(5,10)], [(6,0),(10,5)], [(6,6),(10,10)]]
game = gameInit(plyName, plyArea)


def splitTui(game, tuis):
	print "split tuis"
	game.findHolder(tuis)
	for x in game.players:
		print x.name, 
		for y in x.tuisRound:
			print y.votedName,
		print
	print "return game"
	print
	return game
	
game = splitTui(game, tuis)

def subround(game):
	
	print "cal subroundScore"
	game.calSubRoundScore()
	winner = game.calSubRoundWinner()
	print "winner: "+str(winner)
	game.calSumSubRoundScore(winner)
	for x in game.players:
		print x.name, x.subRoundScore, x.sumSubRoundScore
	return 0
	
subround(game)