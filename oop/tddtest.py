from tuilib import TuiLegit
import math

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)



def abc(input):
	"""
	>>> abc([[(1,1),(2,2),(3,3)],				[(1,1),(2,2),(5,3)],				[(1,1),(2,2),(4,3)],				[(1,1),(2,2),(4,3)],				[(1,1),(2,2),(4,3)],			   [(1,1),(2,2),(5,3)]])
	(1.0, 1.0) [1, 1, 1, 1, 1]
	(2.0, 2.0) [1, 1, 1, 1, 1]
	(5.0, 3.0) [1, 0, 0, 0, 1]
	(4.0, 3.0) [0, 1, 1, 1, 0]
	
	
	>>> abc( [ [(1,1)], [(1.25,1.25)] ] )
	(1.1666666666666667, 1.1666666666666667) [1, 1, 0, 0, 0]

	"""

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
		
		
		
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	