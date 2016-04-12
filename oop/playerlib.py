from tuilib import TuiLegit

class Player:
	"Control palyer stats"
	def __init__(self, name):
		self.name				= name
		self.subRoundScore		= 0
		self.area				= []	# [(x1,y,1),(x2,y2)]
		self.tuisSubRound		= [] 	# tmp for calculate subround score
		self.sumSubRoundScore	= -2
	
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
				 
class GameCtrler:
	# class __doc__
	"Control game mechanic (win/lose)"
	
	def __init__(self, name):
		self.players		= [Player(i) for i in name] # create 4 players
		self.boardScore 	= [] # [ [game score], 10 times ] => [[2,2,-2,-2], [0,0,1,-1], ...]
		self.leader			= 0
		self.subRoundLeft 	= 8
	
	def setArea(self, img):
		i = img.shape[0]  #    Player Index
		j = img.shape[1]  # [   0   |   1   ]
		a = int(i/2)	  # [   3   |   2   ]
		b = int(j/2)
		area = [[(0,0),(a,b)], [(0,b+1),(a,j)], [(a+1,b+1),(i,j)], [(a+1,0),(i,b)]]
		for p,a in zip(self.players, area):
			p.putArea(a)
		
	# ================================== SubRound ==================================
	# what to do when endSubRound
	# 0.) check if this endsubround is also end round
	# 1.) get all tuis in board
	# 2.) find tuis holder
	# 3.) cal tui subround score
	#  3.1) check if tui sell
	# 4.) find winner
	#  4.1) update sumSubRound score
	#  4.2) update subRound left
	
	def endSubRound(self, tuis):
		self.findHolder(tuis)
		self.calSubRoundScore()
		self.findSubRoundWinner()
		self.calSumSubRoundScore()
		self.resetSubRound()
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