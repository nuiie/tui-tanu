import numpy as np
import cv2

img = cv2.imread('juk.jpg',0)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
img2 = cv2.imread('jukR.jpg',0)
cv2.imshow('image',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()