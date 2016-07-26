from tuilib import TuiLegit
import math

class causalBox():
	# class __doc__
	"caussal Box compute previeus frames for more accurate and stability"
	
	def __init__(self, winSize):
		self.winSize		= winSize
		self.thresh			= None
		self.tuis 			= []
		
	def setThresh(self, thresh):
		self.thresh = thresh
	
	def distance(self, p0, p1):
		return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
	
	def feedIn(self, frame):
		for tui in self.tuis: # set reached flag
			tui.reached = False
		
		for pos, name in frame:
			# tui check in
			match = False # set match flag before start matching
			for tui in self.tuis:
				if self.distance(pos,tui.position) <= self.thresh: # if tui match
					tui.posMatched(pos, name)
					match = True
					break
			if match == False: # no tui match
				self.tuis.append(TuiLegit(pos, self.winSize, name)) # append new tui
			
		# tui check up
		for tui in self.tuis:
			if not tui.reached: # add up match flag
				tui.shiftMatchFlagAndName()
			if 1 not in tui.matchFlag: # check to destroy any tui
				self.tuis.remove(tui)