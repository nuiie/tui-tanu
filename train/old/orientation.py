import cv2
import numpy as np

def main(imgName):
	print imgName
	src1 = cv2.imread(imgName,0)
	src2 = cv2.imread(".\\juk_red\\1457369661_96.png",0)
	src1 = np.float32(src1)
	src2 = np.float32(src2) 
	cv2.imshow('a',src1)
	cv2.imshow('b',src2)
	pt = cv2.phaseCorrelate(src1,src2)	
	print pt
	angle = 180.0 * pt[0] / len(src1[0])
	print angle

	k = cv2.waitKey()
	# cv2.imwrite('.\\polar\\'+str(time.time()).replace('.','_')+'.png',img2)
	return 0
	
main(".\\juk_red\\1457369661_66.png")
	
# f = open('.\\new\\text.txt', 'r')
 # for line in f:
	# path = '.\\new\\'+line
	# main(path.strip())