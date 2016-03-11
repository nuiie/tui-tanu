import cv2
import numpy as np
import time

# find contour/ check if circle/ check size/ crop contur/ save

def main(imgName):
	print imgName
	img = cv2.imread(imgName)
	gray = cv2.imread(imgName,0)
	# gray = cv2.medianBlur(gray,3)
	ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	# contour = sorted(contour, key = cv2.contourArea, reverse = True)
	# sort contours by cnt area / img area ratio from max to min
	contours = sorted(contours, key = lambda x: cv2.contourArea(x)/len(thresh[0])**2, reverse = False)
	out = np.zeros_like(thresh)
	print len(contours)
	cv2.drawContours(img,contours,3,(0,255,0), 3)
	for cnt in contours:
		area = cv2.contourArea(cnt)
		tuiCircle = []
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		radius = int(radius)
		minArea = 3.14159*radius*radius*0.6
		maxArea = 3.14159*radius*radius*1.4
		# print 'a/calA : ' + str(area/(3.14159*radius*radius)*100), ' a/imgA: '+ str(area/len(thresh[0])**2*100), area
		if area >= minArea and area <= maxArea and area > img.size*0.1:
			cv2.drawContours(img, [cnt], 0, (0,255,0), 3)

			# copy
			thresh = cv2.bitwise_not(thresh)
			mask = np.zeros_like(thresh) # Create mask where white is what we want, black otherwise
			cv2.drawContours(mask, [cnt], 0, 255, -1) # Draw filled contour in mask
			out = np.zeros_like(thresh) # Extract out the object and place into output image
			out[mask == 255] = thresh[mask == 255]

			break
	cv2.imshow('Output',out)
	cv2.imshow('a',img)
	cv2.waitKey()
	cv2.imwrite('.\\test1\\'+str(time.time()).replace('.','_')+'.png',out)
	
	return 0

	
# f = open('.\\test1\\text.txt', 'r')
# for line in f:
	# path = '.\\test1\\'+line
	# main(path.strip())
	
	
main('.\\test1\\verA41456848424.3718.png')