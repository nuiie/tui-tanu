import numpy as np
import cv2
from matplotlib import pyplot as plt



def run_main():
	blurWinSize = 9
	im = cv2.imread("../Photos/IMG_20160120_133242.jpg", cv2.IMREAD_GRAYSCALE)
	blur = cv2.medianBlur(im,blurWinSize)
	th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,95,2)
	th3 = cv2.medianBlur(th3,blurWinSize)
	titles = ['Original Image', 'medianBlur ('+str(blurWinSize)+')', 'Adaptive Gaussian Thresholding']
	images = [im, blur, th3]
	cv2.namedWindow('4', cv2.WINDOW_NORMAL)
	cv2.imshow('4',th3)
	for i in xrange(3):
		plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()
	

	
	cv2.imwrite('img1.png',th3)
	
	cv2.waitKey()
if __name__ == "__main__":
	run_main()