import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
import random


def polar2cart(r, theta, center):

	x = r  * np.cos(theta) + center[0]
	y = r  * np.sin(theta) + center[1]
	return x, y

def img2polar(img, center, final_radius, initial_radius = None, phase_width = None):

	if initial_radius is None:
		initial_radius = 0
		
	if phase_width is None:
		phase_width = max ( len(img), len(img[0]))
		
	theta , R = np.meshgrid(np.linspace(0, 2*np.pi, phase_width),np.arange(initial_radius, final_radius))

	Xcart, Ycart = polar2cart(R, theta, center)

	Xcart = Xcart.astype(int)
	Ycart = Ycart.astype(int)

	if img.ndim ==3:
		polar_img = img[Ycart,Xcart,:]
		polar_img = np.reshape(polar_img,(final_radius-initial_radius,phase_width,3))
	else:
		polar_img = img[Ycart,Xcart]
		polar_img = np.reshape(polar_img,(final_radius-initial_radius,phase_width))

	return polar_img
	
	
def main(imgName):
	print imgName
	img = cv2.imread(imgName)
	
	center = ( int(len(img)/2) , int(len(img[0])/2) )	
	img2 = img2polar(img, center, int(len(img)/2) )
		

	cv2.imshow('b',img)
	cv2.imshow('a',img2)
		
	
	k = cv2.waitKey()
	cv2.imwrite('.\\polar\\'+str(time.time()).replace('.','_')+'.png',img2)
	return 0
	
# main(".\\binaryImg\\1457206463_18.png")


	
f = open('.\\new\\text.txt', 'r')
for line in f:
	path = '.\\new\\'+line
	main(path.strip())