import cv2
import numpy as np
#GUI
img = np.zeros((300,500,3),np.uint8)
cap = cv2.VideoCapture(0)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


cv2.namedWindow("image")
def nothing(self):
    pass
# create trackbars for color change
cv2.createTrackbar('Hmin','image',0,179,nothing)
cv2.createTrackbar('Smin','image',0,255,nothing)
cv2.createTrackbar('Vmin','image',0,255,nothing)
cv2.createTrackbar('Hmax','image',0,179,nothing)
cv2.createTrackbar('Smax','image',0,255,nothing)
cv2.createTrackbar('Vmax','image',0,255,nothing)

switch = "ON,OFF"

cv2.createTrackbar(switch,'image',0,1,nothing)    
h,s,v = 0,0,0


ix,iy = -1,-1
t=0
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,t
    if event == cv2.EVENT_LBUTTONDOWN:
        t=1
        ix,iy = x,y


# Create a black image, a window and bind the function to window
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

Hmax=0
Smax=0
Vmax=0
Hmin=255
Smin=255
Vmin=255

# setup initial location of window
r,h,c,w = 250,90,400,125  # simply hardcoded the values
track_window = (c,r,w,h)

while(1):
    im = cv2.imread('jukR.jpg')
    cv2.imshow('image',im)
    ret ,img = cap.read()
    hsv2 = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    if(ret == True):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if(s==1):
            cv2.imshow('image2',mask)
            cv2.imshow('image3',img2)
        else:
            cv2.setTrackbarPos('Hmin', 'image', 255)
            cv2.setTrackbarPos('Smin', 'image', 255)
            cv2.setTrackbarPos('Vmin', 'image', 255)
            cv2.setTrackbarPos('Hmax', 'image', 0)
            cv2.setTrackbarPos('Smax', 'image', 0)
            cv2.setTrackbarPos('Vmax', 'image', 0)
        if(t==1):
            i,j,k= hsv2[iy,ix]
            Hmax=max(i,Hmax)
            Smax=max(j,Smax)
            Vmax=max(k,Vmax)
            Hmin=min(i,Hmin)
            Smin=min(j,Smin)
            Vmin=min(k,Vmin)

            cv2.setTrackbarPos('Hmin', 'image', Hmin)
            cv2.setTrackbarPos('Smin', 'image', Smin)
            cv2.setTrackbarPos('Vmin', 'image', Vmin)
            cv2.setTrackbarPos('Hmax', 'image', Hmax)
            cv2.setTrackbarPos('Smax', 'image', Smax)
            cv2.setTrackbarPos('Vmax', 'image', Vmax)
            print(Hmax,Smax,Vmax)
            print(Hmin,Smin,Vmin)

        # get current positions of four trackbars
        Hmin = cv2.getTrackbarPos('Hmin','image')
        Smin = cv2.getTrackbarPos('Smin','image')
        Vmin = cv2.getTrackbarPos('Vmin','image')
        Hmax = cv2.getTrackbarPos('Hmax','image')
        Smax = cv2.getTrackbarPos('Smax','image')
        Vmin = cv2.getTrackbarPos('Vmin','image')
        s = cv2.getTrackbarPos(switch,'image')

        lower_blue = np.array([Hmin-10,Smin-10,Vmin-10])
        upper_blue = np.array([Hmax+10,Smax+10,Vmax+10])
        mask = cv2.inRange(hsv,lower_blue, upper_blue)
        
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

        # apply meanshift to get the new location
        ret, track_window = cv2.CamShift(mask, track_window, term_crit)
        kernel = np.ones((5,5),np.uint8)
        mask2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernel)

        tmp,con,hie = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        img2 = cv2.polylines(img,con,True,255,2)
        t=0

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
