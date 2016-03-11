import numpy as np
import cv2


def set_res(cap, x,y):
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
	return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


cap = cv2.VideoCapture(0)

print set_res(cap,1280,720)





# bg = None
# while(True):
	# # Capture frame-by-frame
	# ret, frame = cap.read()
	
	# # Our operations on the frame come here
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# frame = cv2.medianBlur(frame,5)
	
	# # Display the resulting frame
	# cv2.imshow('frame',frame)
	# if bg != None:
		# cv2.imshow('frame2',frame-bg)
		# cv2.imshow('frame3',bg-frame)
		
	# k = cv2.waitKey(1)
	# if k == ord('q'):
		# break
	# elif k == ord('c'):
		# bg = frame
		# cv2.imshow('capture',bg)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()