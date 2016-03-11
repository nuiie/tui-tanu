# tracking color
# video capture 


import numpy as np
import cv2
url = "http://www.bmatraffic.com/images/clips/10_101_128_24.jpeg"
cap = cv2.VideoCapture(0)

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
r,h,c,w = 250,90,400,125  # simply hardcoded the values
track_window = (c,r,w,h)
upper,lower=1,0
color=[(0, 150, 150),(30,255,255)]
print 'color[lower]=', color[lower]
print 'color[upper]=', color[upper]

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array(color[lower]), np.array(color[upper]))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1) # can't fix data
        mask = cv2.inRange(hsv, np.array(color[lower]), np.array(color[upper]))
		
        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(mask, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        img1 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        img3 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        #cv2.imshow('img2',hsv) #show error
        #cv2.imshow('img2',mask) # white or black
        cv2.imshow('img1: RGB world '+str(color[lower])+' to '+str(color[upper]) ,frame)
        cv2.imshow('img2: mask (black and white only)'+str(color[lower])+' to '+str(color[upper]),mask)
        cv2.imshow('img3: HSV world',hsv)
		
		
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",img2)

    else:
        break

cv2.destroyAllWindows()
cap.release()