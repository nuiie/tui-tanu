import cv2
import numpy as np


def updateCasual(casual,im,num):
	casual.insert(0,im)
	if len(casual) > num:
		casual.pop()	
	return casual

def run_main():
	
	cap = cv2.VideoCapture(0)
	casual = []
	while(True):
		ret, im = cap.read()
		casual = updateCasual(casual,im,10)
		
		
		
		
		cv2.imshow('first',casual[0])
		cv2.imshow('last',casual[len(casual)-1])
		
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
if __name__ == "__main__":
	run_main()