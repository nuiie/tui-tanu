import numpy as np
import cv2
from matplotlib import pyplot as plt


img = cv2.imread("img2.png", cv2.IMREAD_GRAYSCALE)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 1)
dilation = cv2.dilate(img,kernel,iterations = 1)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
titles = ['erosion','dilation','opening','closing']
images = [erosion,dilation,opening,closing]
for i in xrange(4):
	plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
	plt.title(titles[i])
	plt.xticks([]),plt.yticks([])
plt.show()
	
cv2.waitKey()