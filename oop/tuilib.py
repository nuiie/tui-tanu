class Tui:
	"Tui class for each tui. Contain tui's property"
	def __init__(self, name, img=None, type=None):
		self.name 	= name
		self.img 	= img
		self.type 	= 'Undifine'
		
		if type is not None: self.type = type
		
	def displayImg(self):
		print self.img
