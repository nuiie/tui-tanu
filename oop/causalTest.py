from tuilib import TuiLegit
import math

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def tuiCheckIn(pos):
	# if pos match tuis[n]
	# do someting with that tuis[n]
	
	# else create new tuis[n] and append
		

	return 0
	
def tuiCheckUp():
	# check up
	# check if theere is any tuis[n] to destroy
	# check to mod all pos and count all tuis
			
	return 0
	
def input():

	input =  ([[(1,1),(2,2),(3,3)],
				[(1,1),(2,2),(5,3)],
				[(1,1),(2,2),(4,3)],
				[(1,1),(2,2),(4,3)],
				[(1,1),(2,2),(4,3)],
			   [(1,1),(2,2),(5,3)]])
	thresh 	= 0.5
	winSize = 5
	tuis = []
	for frame in input: 
		
		for tui in tuis: # set reached flag
			tui.reached = False
		
		for pos in frame:
			
			# tui check in
			match = False # set match flag before start matching
			for tui in tuis:
				if distance(pos,tui.position) <= thresh: # if tui match
					tui.posMatched(pos)
					match = True
					break
			if match == False: # no tui match
				tuis.append(TuiLegit(pos,winSize)) # append new tui
			
		# tui check up
		for tui in tuis:
			if not tui.reached: # add up match flag
				tui.shiftMatchFlag()
		
			if 1 not in tui.matchFlag: # check to destroy any tui
				tuis.remove(tui)
				
	for tui in tuis:
		print tui.position, tui.matchFlag
			
	
	
input()