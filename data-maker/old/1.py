import cv2
import numpy as np
from matplotlib import pyplot as plt
import os.path


# miscellaneous

def plot(images,titles):
	num_img = len(images)
	
	if num_img != len(titles):
		print "num of titles and images is not equal"
		return 0
	row = int(num_img**0.5+1)
	for i in xrange(num_img):
		plt.subplot(row,row,i+1)
		plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	return plt


# image quality 
	
def Adaptive_Threshold(im,adaptiveWinSize=None):
	if adaptiveWinSize is None:
		adaptiveWinSize = 95
	th = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,adaptiveWinSize,2)
	return th

def medBlur(im,blurWinSize=None):
	if blurWinSize is None:
		blurWinSize = 9
	blur = cv2.medianBlur(im,blurWinSize)
	return blur
	
def morpTrans(img,mode,pow=None,winSize=None):
	if winSize is None:
		winSize = 5
	if pow is None:
		pow = 1
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(winSize,winSize))
	if mode is 1: # erosion
		img = cv2.erode(img,kernel,iterations = pow)
	elif mode is 2: # dilatetion
		img = cv2.dilate(img,kernel,iterations = pow)
	elif mode is 3: # opening
		img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	elif mode is 4: #closing
		img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	else:
		print "MropTrans mode invalid"
		return 0
	return img

	
	
# contour

def fillContour(img):
	hier,contour,hier = cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contour:
		cv2.drawContours(img,[cnt],0,255,-1)
	return img

def findFg(img):
	dist_transform = cv2.distanceTransform(img,cv2.DIST_L2,5)
	ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
	return sure_fg

def markFg(ori,sure_fg,sizeCircle=None):
	sure_fg = np.uint8(sure_fg)
	if sizeCircle is None:
		sizeCircle = 3.25
	hierarchy,contours, hierarchy = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius*sizeCircle)
		img = cv2.circle(ori,center,radius,(0,255,0),2)
	return img,contours
	
	
def extractTui(img,contours):
	tui = []
	
	for cnt in contours:
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius*3.25)
		
		x1 = center[0]-radius
		y1 = center[1]-radius
	
		x2 = center[0]+radius
		y2 = center[1]+radius
		tui.append(img[y1:y2,x1:x2])
	return tui
	
	
def run_main(path):
	images = []
	titles = []
	name = path.split('\\')[-1].split('.')[0]
	# print os.path.exists('..\\Photos\\'+name+'.jpg')
	# name = 'IMG_20160120_133913'
	
	ori = cv2.imread('..\\Photos\\'+name+'.jpg', cv2.IMREAD_GRAYSCALE)
	
	
	
	img = medBlur(ori)
	images.append(img)
	titles.append("0")
	
	img = Adaptive_Threshold(img)	
	images.append(img)
	titles.append("1")
	
	img = medBlur(img)
	images.append(img)
	titles.append("2")
	
	img = morpTrans(img,1)
	images.append(img)
	titles.append("3")
	
	img = morpTrans(img,3)
	images.append(img)
	titles.append("4")
	
	img = morpTrans(img,1)
	images.append(img)
	titles.append("5")
	
	img = fillContour(img)
	images.append(img)
	titles.append("6")
	
	img = morpTrans(img,3,2)
	images.append(img)
	titles.append("7")
	
	img = medBlur(img,15)
	images.append(img)
	titles.append("8")
	
	img = findFg(img)
	images.append(img)
	titles.append("sure_fg")
	
	img,contours = markFg(ori,img)
	
	ori = cv2.imread('..\\Photos\\'+name+'.jpg')
	tuis = extractTui(ori,contours)
	# plot(tuis, range(len(tuis)) ).show()
	
	
	for i,tui in zip(range(len(tuis)),tuis):
		cv2.imwrite(name+'_img_'+str(i)+".png",tui)
	print name
	# if img is None:
		# print "None"
	# else:
		# cv2.namedWindow('a', cv2.WINDOW_NORMAL)
		# cv2.imshow('a',img)
	
	# plot(images,titles).show()
	# blur = cv2.medianBlur(im,9)
	# ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# titles = ['Original Image', 'medianBlur ('+str(9)+')', 'THRESH_OTSU']
	# images = [im, blur, th3]
	# plot(titles,images).show()
	cv2.waitKey()
	
if __name__ == "__main__":
	f = open('..\\Photos\\name.txt', 'r')
	paths = []
	for line in f:
		paths.append(line)
		run_main(line)