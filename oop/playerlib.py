from tuilib import TuiLegit
import numpy as np
import cv2
import copy

class Player:
	"Control palyer stats"
	def __init__(self, name):
		self.name				= name
		self.subRoundScore		= 0
		self.area				= []	# [(x1,y,1),(x2,y2)]
		self.tuisSubRound		= [] 	# all tuis before endRound [[tuiLegit1, tuiLegit2], [.....]] index0:recent 1:previous
		self.sumSubRoundScore	= -2
		self.pColor				= None
	
	def putArea(self,area):
		self.area = area
		
	def putTui(self, tui): # append 1 by 1
		self.tuisSubRound[0].append(copy.copy(tui))
		
	def isInMe(self, point):
		return all([ self.area[0][i] <= point[1-i] <= self.area[1][i] for i in range(2)])
		
	# shouldn't be in player class
	def isNotSell(self): # check if tuis is not against the rules
		return True
		t = self.tuisSubRound
		if len(t) == 0: # no tui found
			return False
		elif len(t) == 1:
			return True
		elif len(t) == 2:
			if t[0].votedName == t[1].votedName:
				return True
			else:
				return False
		elif len(t) == 3:
			if all(x.votedName == "R juk" for x in t) or all(x.votedName == "B juk" for x in t):
				return True
			elif all(x in [n.votedName for n in t] for x in ["R T","R Fly","R Ele"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["B T","B Fly","B Ele"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["R Boat","R Horse","R Phao"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["B Boat","B Horse","B Phao"]):
				return True
			else:
				return False
		elif len(t) == 4:
			if all(x.votedName == "R juk" for x in t) or all(x.votedName == "B juk" for x in t):
				return True
			elif all(x in [n.votedName for n in t] for x in ["R T","R Fly","R Ele"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["B T","B Fly","B Ele"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["R Boat","R Horse","R Phao"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["B Boat","B Horse","B Phao"]):
				return True
			else:
				return False
		elif len(t) == 5:
			if all(x.votedName == "R juk" for x in t) or all(x.votedName == "B juk" for x in t):
				return True
			elif all(x in [n.votedName for n in t] for x in ["R T","R Fly","R Ele"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["B T","B Fly","B Ele"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["R Boat","R Horse","R Phao"]):
				return True
			elif all(x in [n.votedName for n in t] for x in ["B Boat","B Horse","B Phao"]):
				return True
			else:
				return False
		else:
			return False
			
	def putSubRoundScore(self, score):
		self.subRoundScore = score
	
	def getSubRoundScore(self): 
		score = 0
		for tui in self.tuisSubRound[0]:
			score += tui.getScore()
		return score
	
	def putColor(self, color):
		self.pColor = color
		
class GameCtrler:
	# class __doc__
	"Control game mechanic (win/lose)"
	
	def __init__(self, name):
		self.players		= [Player(i) for i in name] # create 4 players
		self.boardScore 	= [] # [ [game score], 10 times ] => [[2,2,-2,-2], [0,0,1,-1], ...]
		self.leader			= 0
		self.subRoundLeft 	= 8
		self.bScoreImg		= None
		self.pScoreImg		= None

	def setArea(self, img): # set player area and create score img
		i = img.shape[0]  #    Player Index
		j = img.shape[1]  # [   0   |   1   ]
		a = int(i/2)	  # [   3   |   2   ]
		b = int(j/2)
		area = [[(0,0),(a,b)], [(0,b+1),(a,j)], [(a+1,b+1),(i,j)], [(a+1,0),(i,b)]]
		for p,a in zip(self.players, area):
			p.putArea(a)	
		h = img.shape[0] # set scoreImg
		w = img.shape[1]
		self.pScoreImg = np.zeros((h,w,3), np.uint8)
		self.bScoreImg = np.zeros((h,w*0.5,3), np.uint8)
	
	# ================================== SubRound ==================================
	def endSubRound(self, tuis):
		self.resetSubRound()
		self.findHolder(tuis)
		self.calSubRoundScore()
		self.findSubRoundWinner()
		self.calSumSubRoundScore()
		if self.subRoundLeft <= 0:
			self.endRound()
	
	def findHolder(self, tuis):
		holdCount = 0
		for t in tuis:  
			for p in self.players:
				if p.isInMe(t.position):
					p.putTui(t)
					holdCount += 1
					break
		print str(len(tuis))+"tuis found.", str(holdCount)+"found holders"
		
	def calSubRoundScore(self): # calculate SubroundScore
		for plyr in self.players:
			if plyr.isNotSell(): 	#check if player sell tuis
				subRoundScoreTmp = plyr.getSubRoundScore() # get score if not sell
				plyr.putSubRoundScore(subRoundScoreTmp)
			else:
				plyr.putSubRoundScore(0)
	
	def findSubRoundWinner(self):
		v=list([x.subRoundScore for x in self.players])
		self.leader = v.index(max(v))
		
	def calSumSubRoundScore(self): # need more secure
		winnerIndex = self.leader
		numEat = len(self.players[winnerIndex].tuisSubRound[0])
		self.players[winnerIndex].sumSubRoundScore += numEat
		self.subRoundLeft -= numEat
	
	def resetSubRound(self):
		for p in self.players:
			p.tuisSubRound.insert(0,[])
			subRoundScore	= 0
	# ==============================================================================
	
	# ==================================== Round ====================================
	def endRound(self):
		self.putRoundScore()
		self.resetRoundStats()
		if len(self.boardScore)%10 == 0:
			self.endBoard()
			
	def putRoundScore(self):
		self.boardScore.append([s.sumSubRoundScore for s in self.players])
	
	def resetRoundStats(self): # player stats + subRound left
		for p in self.players:
			p.sumSubRoundScore = -2
			p.tuisSubRound = [[]]
		self.subRoundLeft = 8
	# ==============================================================================
	
	# ================================== endBoard =================================
	def endBoard(self):
		self.boardScore.append([sum([ x[i] for x in self.boardScore]) for i in range(4)])

	# ==============================================================================
	
	# ================================== Show Score ================================
	def getScoreBoard(self):
		self.setColor()
		self.writePlayerStats()
		self.writeBoardStats()
		return np.concatenate((self.pScoreImg,self.bScoreImg), axis=1)
		
	def setColor(self):
		self.setPColor()
		self.setPScoreImgColor()
	
	def setPScoreImgColor(self):
		for p in self.players:
			a = p.area
			self.pScoreImg[a[0][0]:a[1][0], a[0][1]:a[1][1]] = p.pColor
		
	def setPColor(self):
		color = [(0,255,255), (255,0,0), (0,0,255), (0,255,0)] # color : yellow blue red green
		for p,c in zip(self.players,color):
			p.pColor = c
		
	def writePlayerStats(self):
		rts = len(self.players[0].tuisSubRound)  # rts: row to show
		rsw = 35 # rw: row space width
		for p in self.players: # wirte name
			cv2.putText(self.pScoreImg, p.name+" "+str(p.sumSubRoundScore), (p.area[0][1],p.area[0][0]+rsw), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(255,255,255),2)
		# print rts
		for i in range(rts): # write subround score
			for p in self.players:
				cv2.putText(self.pScoreImg, str([t.votedName for t in p.tuisSubRound[i]]), (p.area[0][1],p.area[0][0]+rsw*(i+2)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
				
	def writeBoardStats(self):
		rsw = 50 # rw: row space width
		cv2.putText(self.bScoreImg, "subRound Left: "+str(self.subRoundLeft), (0,rsw), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
		for i in range(len(self.boardScore)): # print write board score
			cv2.putText(self.bScoreImg, str(self.boardScore[i]), (0,0+rsw*(i+2)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
			if i == 4:
				cv2.putText(self.bScoreImg, "---------------------", (0,0+rsw/2+rsw*(i+2)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
			elif i == 9:
				cv2.putText(self.bScoreImg, "---------------------", (0,0+rsw/2+rsw*(i+2)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
			elif i == 10:
				cv2.putText(self.bScoreImg, "=====================", (0,0+rsw/2+rsw*(i+2)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
			