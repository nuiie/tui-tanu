import cv2
import numpy as np
 

def main(input):
	ori = cv2.imread(input,0)
	size = np.size(ori)
	skel = np.zeros(ori.shape,np.uint8)
	ori = cv2.medianBlur(ori,3)
	ret,img = cv2.threshold(ori,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	img = cv2.bitwise_not(img)
	cv2.imshow("img",img)
	element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	done = False
	 
	while( not done):
		eroded = cv2.erode(img,element)
		temp = cv2.dilate(eroded,element)
		temp = cv2.subtract(img,temp)
		skel = cv2.bitwise_or(skel,temp)
		img = eroded.copy()
	 
		zeros = size - cv2.countNonZero(img)
		if zeros==size:
			done = True
	return skel
	
	
def run():
	img1 = '.\\pic\\b.png'
	img2 = '.\\pic\\a.png'
	a2 = main(img2)
	a1 = main(img1)
	cv2.imshow("1",a1)
	cv2.imshow("2",a2)
	# cv2.imwrite('a.png',a1)
	# cv2.imwrite('b.png',a2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
run()