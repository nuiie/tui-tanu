import cv2
import numpy as np
from matplotlib import pyplot as plt


def run_main():
	img = cv2.imread('figure_1.png',0)
	temp = cv2.imread('IMG_20160120_133913_img_0.png',0)
	# blur = cv2.GaussianBlur(img,(13,13),0)
	# ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	ret3,th4 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	cv2.imshow('b',temp)
	cv2.imshow('c',th4)
	cv2.imshow('a',img)
	cv2.waitKey()
	return 0
	
	
if __name__ == "__main__":
	run_main()