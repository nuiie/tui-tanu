import cv2
import numpy as np


def nuiMome(imgName):
	img = cv2.imread(imgName,0)
	a = cv2.HuMoments( cv2.moments(img,binaryImage = True) ).flatten()
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

	
def run2(path):
	ret = nuiMome(path)
	# print name+',',
	print ' '.join(str(p) for p in ret)	
	print 0
	return 0
	
# def run(path):
	# # path = ['a.png','b.png','c.png','d.png','e.png','f.png','g.png','h.png','i.png','j.png','k.png','l.png','m.png','n.png']
	# ret = nuiMome(path)
	# ret2 = nuiMome('.\\new\\horA41457370062.630.png')
	# # for img in path:
		# # ret2 = nuiMome(img)
	# print test1(ret,ret2),test2(ret,ret2),test3(ret,ret2),path
	
	
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	
name = "jukblack"
f = open('.\\'+name+'\\text.txt', 'r')
for line in f:
	path = '.\\'+name+'\\'+line
	run2(path.strip())