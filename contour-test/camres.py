import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def set_res(cap, x,y):
    cap.set(CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(CAP_PROP_FRAME_WIDTH)),str(cap.get(CAP_PROP_FRAME_HEIGHT))
	
set_res(cap,1280,720)