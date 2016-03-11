import cv2
import numpy as np
from matplotlib import pyplot as plt

def main():
	temp = cv2.imread('IMG_20160120_133913_img_6.png',0)
	img = cv2.imread('IMG_20160120_132852_img_4.png',0)
	
	sift = cv2.xfeatures2d.SIFT_create()
	return 0
	
	
main()
