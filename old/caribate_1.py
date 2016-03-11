import cv2
import numpy as np

cap = cv2.VideoCapture(0)

mouseDown = False
Hmax=0
Smax=0
Vmax=0
Hmin=255
Smin=255
Vmin=255

upper,lower=1,0
color=[(0, 150, 150),(30,255,255)]

ix,iy = -1,-1
# mouse callback function
def draw_circle(event,x,y,flags,param):
	global ix,iy,mouseDown
	if event == cv2.EVENT_LBUTTONDOWN:
		mouseDown = True
		ix,iy = x,y
		print "mouseDown"

# Create a black clickWin, a window and bind the function to window
cv2.namedWindow('clickWin')
cv2.setMouseCallback('clickWin',draw_circle)


while(1):
	
	# Take each frame
	ret, frame = cap.read()
	cv2.imshow('original',frame)
	
	
	if ret == True:
		
		#  Filter
		frame = cv2.medianBlur(frame,5)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
		
		
		
		if mouseDown == True:
			i,j,k= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[iy,ix]
			Hmax=max(i,Hmax)
			Smax=max(j,Smax)
			Vmax=max(k,Vmax)
			Hmin=min(i,Hmin)
			Smin=min(j,Smin)
			Vmin=min(k,Vmin)
			

			color=[(Hmin, Smin, Vmin),(Hmax,Smax,Vmax)]
			print i,j,k
			print "ColorLower", color[lower]
			print "ColorUpper", color[upper]
			
			
		mouseDown = False
		
		# Mask
		mask = cv2.inRange(hsv, np.array(color[lower]), np.array(color[upper]))
		
		
		# Dispaly
		cv2.imshow('clickWin',frame)
		cv2.imshow('mask',mask)
		
		# Esc to exit
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
	else:
		print "No return from camera."
		break
cv2.destroyAllWindows()