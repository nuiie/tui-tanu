import cv2
import numpy as np




def main():
	img = cv2.imread('verA4.png',0)
	img = cv2.medianBlur(img,1)
	cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
	minCalRad = np.round(len(img[0])/24)
	maxCalRad = np.round(len(img[0])/10)

	circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,minCalRad*2,param1=50,param2=30,minRadius=minCalRad,maxRadius=maxCalRad)
	if circles is not None:
		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
			# draw the outer circle
			cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
			# draw the center of the circle
			cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
	else:
		print 'No circle detected'
	cv2.imshow('detected circles',cimg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

main()