import numpy as np
import cv2


class Tui:
	"Tui class for each tui. Contain tui's property"
	
	def __init__(self, rawImg, position):
	
		self.rawImg 			= rawImg
		self.position			= position
		self.gray				= cv2.cvtColor(rawImg,cv2.COLOR_BGR2GRAY)
		self.hsv				= cv2.cvtColor(rawImg,cv2.COLOR_BGR2HSV)
		_, self.thresh			= cv2.threshold(self.gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		self.boardDetect		= rawImg.copy()
		self.letter				= np.zeros_like(rawImg)
		self.huMoment			= None
		self.name				= None
	
	
	def getLetter(self):
	
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
				# break
		
		
	def getHuMoment(self):
		a = cv2.HuMoments( cv2.moments(self.letter,binaryImage = True) ).flatten()
		self.huMoment = -np.sign(a)*np.log10(np.abs(a))