from tuilib import TuiLegit
import math

class causalBox():
	# class __docc__
	"caussal Box compute previeus frames for more accurae and stability"
	
	
	
	def __init__(self, winSize, tuis, thresh):
		
		
	def distance(p0, p1):
		return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
	
		
	def feedIn(tuis, frame, thresh, winSize):
		# causal position box for stablize tui marking position
		
		for tui in tuis: # set reached flag
			tui.reached = False
		
		for pos, name in frame:
			# tui check in
			match = False # set match flag before start matching
			for tui in tuis:
				if distance(pos,tui.position) <= thresh: # if tui match
					tui.posMatched(pos, name)
					match = True
					break
			if match == False: # no tui match
				tuis.append(TuiLegit(pos, winSize, name)) # append new tui
			
		# tui check up
		for tui in tuis:
			if not tui.reached: # add up match flag
				tui.shiftMatchFlagAndName()
			if 1 not in tui.matchFlag: # check to destroy any tui
				tuis.remove(tui)