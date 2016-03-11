import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	
	blur = cv2.blur(frame,(5,5))
	guss = cv2.GaussianBlur(frame,(5,5),0)
	median = cv2.medianBlur(frame,5)
	bila = cv2.bilateralFilter(frame,9,75,75)

	
	# Display the resulting frame
	cv2.imshow('frame',frame)
	cv2.imshow('blur',blur)
	cv2.imshow('guss',guss)
	cv2.imshow('median',median)
	cv2.imshow('bila',bila)
	
	
	k = cv2.waitKey(1)
	if k == ord('q'):
		break
	elif k == ord('c'):
		bg = frame
		cv2.imshow('capture',bg)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()