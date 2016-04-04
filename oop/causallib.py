from tuilib import Tui

class causalBox():
	# class __docc__
	"caussal Box compute previeus frames for more accurae and stability"
	
	
	
	def __init__(self,windowSize,a4Size):
		position 	= []	# 0:current 1:previeus
		windowSize 	= windowSize
		sumDistance = None
		a4Size 		= size
		legitTui	= []
		
	def putPos(self, pos): # stablize pos before put in
		n = len(self.position)
		maxSize = self.windowSize
	
		if n < maxSize: # fill up
			self.position.insert(0,pos)
		
		elif n = maxSize: # calcualte before fill
			self.position.pop()
			
		elif n > maxSize: 
			print "len pos > windowSize"
		