from tuilib import TuiLegit

class Player:
	"Control palyer stats"
	def __init__(self, name, area):
		self.name				= name
		self.subRoundScore		= []	# contain subround score [0]:current [1]:last subround and so on
		self.area				= area	# [(x1,y,1),(x2,y2)]
		self.tuisRound			= [] 	# tmp for calculate subround score
		self.sumSubRoundScore	= -2
		
	def putTui(self, tui): # append 1 by 1
		self.tuisRound.append(tui)
		
	def isInMe(self, point):
		return all([ self.area[0][i] <= point[i] <= self.area[1][i] for i in range(2)])
		
	def isNotSell(self): # check if tuis is not against the rules
		return True # need rules
		
	def putSubRoundScore(self, score):
		self.subRoundScore.insert(0,score)
	
	def getSubRoundScore(self):
		score = 0
		for tui in self.tuisRound:
			score += tui.getScore()
		return score
	
class ScoreBoard:
	"Controll score board"
	def __init__(self):
		self.boardScore	= []
				 
class GameCtrler:
	# class __doc__
	"Control game mechanic (win/lose)"
	
	def __init__(self, name, area):
		self.players	= [Player(i,j) for i,j in zip(name,area)] # create 4 players
		self.boardScore = ScoreBoard()
		self.leader		= 0
		
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
	
	def calSubRoundWinner(self):
		v=list([x.subRoundScore[0] for x in self.players])
		self.leader = v.index(max(v))
		return self.leader
				
	def calSumSubRoundScore(self, winner):
		self.players[winner].sumSubRoundScore += len(self.players[winner].tuisRound)
		return 0
	
	def endRound(self):
		return 0
		
	def endBoard(self):
		return 0