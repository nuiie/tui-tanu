import cv2
import numpy as np

def main(imgName):
	img = cv2.imread(imgName)
	gray = cv2.imread(imgName,0)
	ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	print 'img size: '+str(len(img))+'*'+str(len(img[0]))
	cv2.circle(img, (len(img)/2,len(img)/2), len(img)/3, (0,0,255))
	cv2.imshow('a',thresh)
	cv2.imshow('b',img)
	cv2.waitKey()
	return 0
	
	
main('.\\test1\\verA41456848424.3713.png')