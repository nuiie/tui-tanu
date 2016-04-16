from tuilib import TuiLegit
import numpy as np

class Player:
	"Control palyer stats"
	def __init__(self, name):
		self.name				= name
		self.subRoundScore		= 0
		self.area				= []	# [(x1,y,1),(x2,y2)]
		self.tuisSubRound		= [] 	# all tuis before endRound [[tuiLegit1, tuiLegit2], [.....]]
		self.sumSubRoundScore	= -2
		self.pColor				= None
	
	def putArea(self,area):
		self.area = area
		
	def putTui(self, tui): # append 1 by 1
		self.tuisSubRound.append(tui)
		
	def isInMe(self, point):
		return all([ self.area[0][i] <= point[i] <= self.area[1][i] for i in range(2)])
		
	# shouldn't be in player class
	def isNotSell(self): # check if tuis is not against the rules
		return True # need rules
		
	def putSubRoundScore(self, score):
		self.subRoundScore = score
	
	def getSubRoundScore(self): 
		score = 0
		for tui in self.tuisSubRound:
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
		self.bScoreImg = np.zeros((h,w,3), np.uint8)
		self.pScoreImg = np.zeros((h,w*0.5,3), np.uint8)
	
	# ================================== SubRound ==================================
	# what to do when endSubRound # !!!! THIS COMMEND IS NOT UP TO DATE !!!!!
	# 0.) check if this endsubround is also end round
	# 1.) get all tuis in board
	# 2.) find tuis holder
	# 3.) cal tui subround score
	#  3.1) check if tui sell  # SECQUENCE HAS BEEN CHANGED
	# 4.) find winner
	#  4.1) update sumSubRound score
	#  4.2) update subRound left
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
		for tui in tuis:  
			for player in self.players:
				if player.isInMe(tui.position):
					player.putTui(tui)
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
		numEat = len(self.players[winnerIndex].tuisSubRound)
		self.players[winnerIndex].sumSubRoundScore += numEat
		self.subRoundLeft -= numEat
	
	def resetSubRound(self):
		for p in self.players:
			p.tuisSubRound	= []
			subRoundScore	= 0
	# ==============================================================================
	
	# ==================================== Round ====================================
	# what to do when endRound
	# 1.) put sumSubRound of each player score to score board
	# 2.) reset player subround stats
	def endRound(self):
		self.putRoundScore()
		self.resetRoundStats()
		if len(self.boardScore)%10 == 0:
			self.endBoard()
		
	def putRoundScore(self):
		roundScore = [x.sumSubRoundScore for x in self.players]
		self.boardScore.append(roundScore)
		
	def resetRoundStats(self): # player stats + subRound left
		for p in self.players:
			p.sumSubRoundScore = -2
		self.subRoundLeft = 8
	# ==============================================================================
	
	# ================================== endBoard =================================
	# what to do when endBoard
	# 1.) sum score for each player	
	def endBoard(self):
		print "endBoard"
		return 0
	# ==============================================================================
	
	# ================================== Show Score ================================
	def getScoreBoard(self):
		self.setColor()
		self.writePlayerStats()
		self.writeBoardStats()
		return np.concatenate((self.pScoreImg,self.bScoreImg), axis=1)
	
	def setColor(self):
		self.setPColor()
		self.setBColor()
	
	def setBColor(self):
		for p in self.players:
			a = p.area
			self.bScoreImg[a[0][0]:a[1][0], a[0][1]:a[1][1]] = p.pColor
		
	def setPColor(self):
		color = [(0,255,255), (255,0,0), (0,0,255), (0,255,0)] # color : yellow blue red green
		for p,c in zip(self.players,color):
			p.pColor = c
		
	def writePlayerStats(self):
		rts = len(self.players[0].tuisSubRound)  # rts: row to show
		rsw = 25 # rw: row space width
		for p in self.players: # wirte name
				cv2.putText(self.pScoreImg, p.name, (p.area[0][1],p.area[0][0]+rsw, cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
		for i in range(rts): # write subround score
			for p in self.players:
				cv2.putText(self.pScoreImg,[t.votedName for t in p.tuisSubRound[i]], (p[0][1],p[0][0]+rsw*(i+2)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
	
	def writeBoardStats(self):
		rsw = 25 # rw: row space width
		cv2.putText(self.bScoreImg, "subRound Left: "+str(self.subRoundLeft), (0,rsw), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
		for i in range(len(self.boardScore)): # print write board score
				cv2.putText(self.bScoreImg, self.boardScore[i], (0,0+rsw*(i+2)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
			