from tuilib import Tui

class Player:
	def __init__(self, name, position):
		self.name			= name
		self.roundScore		= []
		self.position		= position # [(x1,y,1),(x2,y2)]
		self.roundScore		= 0
		self.tuisRound		= []
		
	def putTui(self, tui): # append 1 by 1
		self.tuisRound.append(tui)
		
	def isInMe(self, point):
		print point
		return all([ self.position[0][i] <= point[i] <= self.position[1][i] for i in range(2)])
			
class ScoreBoard:
	def __init__(self, name, position):
		self.players		= [Player(i,j) for i,j in zip(name,position)] # create 4 players
		self.boardScore		= []
		

	def findHolder(self, tuis):
		holdCount = 0
		for tui in tuis:
			for player in self.players:
				if player.isInMe(tui.position[1]):
					player.putTui(tui)
					holdCount += 1
					break
		print str(len(tuis))+"tuis found.", str(holdCount)+"found holders"
		
		
	def endRound(self):
		# when end of round 
		# 1 calculate point for each player
		# 2 rechek player status
		# 3 update scoreboard
		
		return 0