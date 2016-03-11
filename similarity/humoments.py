import cv2
import numpy as np


def nuiMome(imgName):
	img = cv2.imread(imgName)
	gray = cv2.imread(imgName,0)
	gray = cv2.medianBlur(gray,3)
	ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	thresh = cv2.bitwise_not(thresh)
	a = cv2.HuMoments( cv2.moments(thresh) ).flatten()
	logHu = -np.sign(a)*np.log10(np.abs(a))
	return logHu

def test1(a,b):
	sum = 0
	for i,j in zip(a,b):
		sum = sum + np.absolute(1/i-1/j)
	return sum

def test2(a,b):
	sum = 0
	for i,j in zip(a,b):
		sum = sum + np.absolute(i-j)
	return sum

def test3(a,b):
	return max([ np.absolute(ma-mb)/np.absolute(ma) for ma,mb in zip(a,b) ])
	
	
def run():
	path = ['a.png','b.png','c.png','d.png','e.png','f.png','g.png','h.png','i.png','j.png','k.png','l.png','m.png','n.png']
	ret = nuiMome('4.png')
	for img in path:
		ret2 = nuiMome(img)
		print img,[test1(ret,ret2),test2(ret,ret2),test3(ret,ret2)]
	
	# print temp
	# print ret2
	
	
	
	
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	
run()