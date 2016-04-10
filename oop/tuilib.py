import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier
from collections import Counter

class Tui:
	"Tui class for each tui. Contain tui's property"
	
	def __init__(self, rawImg, position):
	
		self.rawImg 			= rawImg
		self.position			= position # [h, center] -> ['h', (x1,y1)]
		self.gray				= cv2.cvtColor(rawImg,cv2.COLOR_BGR2GRAY)
		self.hsv				= cv2.cvtColor(rawImg,cv2.COLOR_BGR2HSV)
		_, self.thresh			= cv2.threshold(self.gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		self.boardDetect		= rawImg.copy()
		self.letter				= np.zeros_like(rawImg)
		self.huMoment			= None
		self.name				= None
	
	def getLetter(self):
		if self.thresh is None:
			print "no thresh for getLetter"
			return 0
		contours, hierarchy = cv2.findContours( self.thresh.copy() ,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		
		# sort contours by cnt area / img area ratio from max to min
		contours = sorted(contours, key = lambda x: cv2.contourArea(x)/self.thresh.size, reverse = False)
		
		
		for cnt in contours:
			area = cv2.contourArea(cnt)
			
			# area calculation
			(x,y),radius = cv2.minEnclosingCircle(cnt)
			radius = int(radius)
			minArea = 3.14159*radius*radius*0.6
			maxArea = 3.14159*radius*radius*1.4
			
			# if actual area is close enough to 2*pi*r area && area > 10% of pic
			if area >= minArea and area <= maxArea and area > self.thresh.size*0.1:

				# copy
				thresh = cv2.bitwise_not(self.thresh)
				mask = np.zeros_like(thresh) 				# Create mask where white is what we want, black otherwise
				cv2.drawContours(mask, [cnt], 0, 255, -1) 	# Draw filled contour in mask
				self.letter = np.zeros_like(thresh) 				# Extract out the object and place into output image
				self.letter[mask == 255] = thresh[mask == 255]

	def getHuMoment(self):
		a = cv2.HuMoments( cv2.moments(self.letter,binaryImage = True) ).flatten()
		self.huMoment = -np.sign(a)*np.log10(np.abs(a))
		
	def getTuiName(self, classifier):
		if self.huMoment is None:
			print 'tui has no huMoment dont get tui name just yet'
		else:
			prediction = str(int(classifier.predict(self.huMoment.reshape(1,-1)))) # reshape for single sample 
			
			if prediction == '2':
				self.name = 'R T'
			elif prediction == '3':
				self.name = 'B T'
			elif prediction == '4':
				self.name = "R Fly"
			elif prediction == '5':
				self.name = "B Fly"
			elif prediction == '6':
				self.name = 'R Ele'
			elif prediction == '7':
				self.name = "B Ele"
			elif prediction == '8':
				self.name = "R Boat"
			elif prediction == '9':
				self.name = "B Boat"
			elif prediction == '10':
				self.name = "R Horse"
			elif prediction == '11':
				self.name = "B Horse"
			elif prediction == '12':
				self.name = "R Phao"
			elif prediction == '13':
				self.name = "B Phao"
			elif prediction == '14':
				self.name = "R juk"
			elif prediction == '15':
				self.name = "B juk"
			else:
				self.name = prediction
				
class TuiLegit:
	
	def __init__(self, pos, winSize, name):
		self.position			= pos #(float(pos[0]),float(pos[1]))
		self.winSize			= winSize
		self.matchFlag			= [1]+[0]*(winSize-1) # set 1's flag for last frame and 0's for prevoius
		self.reached			= True
		self.name				= [name]+[None]*(winSize-1)
		self.votedName			= None
		self.score				= 0
	
	def posMatched(self, pos, name): # update pos
		# wight average position
		w1 = 5 # weight of old pos
		w2 = 2 # weight of new pos
		self.position = (int((w1*self.position[0] + w2*pos[0])/float(w1+w2)), int((w1*self.position[1] + w2*pos[1])/float(w1+w2)))
		self.matchFlag.insert(0,1) 	# set match flag
		self.matchFlag.pop()		# set match flag
		self.name.insert(0,name) 	# set name
		self.name.pop()				# set name
		self.reached = True
		
	def shiftMatchFlagAndName(self):
		self.matchFlag.insert(0,0) 	# set match flag
		self.matchFlag.pop()		# set match flag
		self.matchFlag.insert(0,None) 	# set name
		self.matchFlag.pop()			# set name
		self.reached = True
		
	def isLegit(self, n=None):
		if n is not None:
			return self.matchFlag.count(1) >= n
		else:
			return self.matchFlag.count(1) >= winSize*0.8
			
	def getVotedName(self):
		data = Counter(self.name)
		self.votedName = data.most_common(1)
		return self.votedName
		
	def getScore(self):
		if self.votedName = "B juk"
			self.score = 1
		elif self.votedName = "R juk"
			self.score = 2
		elif self.votedName = "B Phao"
			self.score = 3
		elif self.votedName = "R Phao"
			self.score = 4
		elif self.votedName = "B Horse"
			self.score = 5
		elif self.votedName = "R Horse"
			self.score = 6
		elif self.votedName = "B Boat"
			self.score = 7
		elif self.votedName = "R Boat"
			self.score = 8
		elif self.votedName = "B Ele"
			self.score = 9
		elif self.votedName = 'R Ele'
			self.score = 10
		elif self.votedName = "B Fly"
			self.score = 11
		elif self.votedName	= "R Fly"
			self.score = 12
		elif self.votedName = 'B T'
			self.score = 13
		elif self.votedName = 'R T'
			self.score = 14
		else:
			self.score = 0
		return self.score