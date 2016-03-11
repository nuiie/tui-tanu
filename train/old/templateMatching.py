import cv2
import numpy as np

def main(imgName):
	print imgName
	template = cv2.imread(".\\juk_red\\1457369661_96.png",0)
	img = cv2.imread(imgName,0)
	imgextend = np.concatenate((img, img), axis=1)
	imgextend = np.concatenate((imgextend, imgextend), axis=0)
	methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
	method = eval(methods[5]) # 1 3 4 5
	
	res = cv2.matchTemplate(imgextend,template,method)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	
	
	# cv2.namedWindow('template',cv2.WINDOW_NORMAL)
	# cv2.namedWindow('imgextend',cv2.WINDOW_NORMAL)
	# cv2.namedWindow('res',cv2.WINDOW_NORMAL)
	# cv2.imshow('template',template)
	# cv2.imshow('imgextend',imgextend)
	# cv2.imshow('res',res)

	k = cv2.waitKey()
	return 0
	
# main(".\\juk_red\\1457369661_66.png")
	
f = open('.\\juk_black\\text.txt', 'r')
for line in f:
	path = '.\\juk_black\\'+line
	main(path.strip())