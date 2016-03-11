import cv2
import numpy as np
#GUI
img = np.zeros((300,500,3),np.uint8)
img = cv2.imread('jukR.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.namedWindow("image")
def nothing(self):
    pass

def setpos():
    cv2.setTrackbarPos('Hmin', 'image', Hmin[len(Hmin)-1])
    cv2.setTrackbarPos('Smin', 'image', Smin[len(Smin)-1])
    cv2.setTrackbarPos('Vmin', 'image', Vmin[len(Vmin)-1])
    cv2.setTrackbarPos('Hmax', 'image', Hmax[len(Hmax)-1])
    cv2.setTrackbarPos('Smax', 'image', Smax[len(Smax)-1])
    cv2.setTrackbarPos('Vmax', 'image', Vmax[len(Vmax)-1])
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

Hmax=[0]
Smax=[0]
Vmax=[0]
Hmin=[255]
Smin=[255]
Vmin=[255]
Hmax_re=[]
Smax_re=[]
Vmax_re=[]
Hmin_re=[]
Smin_re=[]
Vmin_re=[]

while(1):
    if(s==1):
        cv2.imshow('image',img)
        cv2.imshow('image2',mask)
    else:
        cv2.setTrackbarPos('Hmin', 'image', 255)
        cv2.setTrackbarPos('Smin', 'image', 255)
        cv2.setTrackbarPos('Vmin', 'image', 255)
        cv2.setTrackbarPos('Hmax', 'image', 0)
        cv2.setTrackbarPos('Smax', 'image', 0)
        cv2.setTrackbarPos('Vmax', 'image', 0)
    if(t==1):
        Hmax_re=[]
        Smax_re=[]
        Vmax_re=[]
        Hmin_re=[]
        Smin_re=[]
        Vmin_re=[]
        i,j,k= hsv[iy,ix]
        Hmax.append(max(i,Hmax[len(Hmax)-1]))
        Smax.append(max(j,Smax[len(Smax)-1]))
        Vmax.append(max(k,Vmax[len(Vmax)-1]))
        Hmin.append(min(i,Hmin[len(Hmin)-1]))
        Smin.append(min(j,Smin[len(Smin)-1]))
        Vmin.append(min(k,Vmin[len(Vmin)-1]))
        setpos()
        print("max")
        print(Hmax[len(Hmax)-1],Smax[len(Smax)-1],Vmax[len(Vmax)-1])
        print("min")
        print(Hmin[len(Hmin)-1],Smin[len(Smin)-1],Vmin[len(Vmin)-1])

        temp,contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if(len(contours)>0):
            for i in range(len(contours)):
                if(cv2.contourArea(contours[i])>100):
                    print(cv2.contourArea(contours[i]))

    # get current positions of four trackbars
    if(Hmin[len(Hmin)-1] != cv2.getTrackbarPos('Hmin','image') or Smin[len(Smin)-1] != cv2.getTrackbarPos('Smin','image') or Vmin[len(Vmin)-1] != cv2.getTrackbarPos('Vmin','image') or Hmax[len(Hmax)-1] != cv2.getTrackbarPos('Hmax','image') or Smax[len(Smax)-1] != cv2.getTrackbarPos('Smax','image') or Vmax[len(Vmax)-1] != cv2.getTrackbarPos('Vmax','image')):
        Hmin.append(cv2.getTrackbarPos('Hmin','image'))
        Smin.append(cv2.getTrackbarPos('Smin','image'))
        Vmin.append(cv2.getTrackbarPos('Vmin','image'))
        Hmax.append(cv2.getTrackbarPos('Hmax','image'))
        Smax.append(cv2.getTrackbarPos('Smax','image'))
        Vmax.append(cv2.getTrackbarPos('Vmax','image'))

        
    s = cv2.getTrackbarPos(switch,'image')

    lower_blue = np.array([Hmin[len(Hmin)-1],Smin[len(Smin)-1],Vmin[len(Vmin)-1]])
    upper_blue = np.array([Hmax[len(Hmax)-1],Smax[len(Smax)-1],Vmax[len(Vmax)-1]])
    mask = cv2.inRange(hsv,lower_blue, upper_blue)
    t=0

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif( k == ord('z') or k == ord('Z') )and len(Hmax)-1 >0:
        Hmax_re.append(Hmax.pop(len(Hmax)-1))
        Smax_re.append(Smax.pop(len(Smax)-1))
        Vmax_re.append(Vmax.pop(len(Vmax)-1))
        Hmin_re.append(Hmin.pop(len(Hmin)-1))
        Smin_re.append(Smin.pop(len(Smin)-1))
        Vmin_re.append(Vmin.pop(len(Vmin)-1))
        setpos()
        print("max")
        print(Hmax[len(Hmax)-1],Smax[len(Smax)-1],Vmax[len(Vmax)-1])
        print("min")
        print(Hmin[len(Hmin)-1],Smin[len(Smin)-1],Vmin[len(Vmin)-1])

    elif( k == ord('x') or k == ord('X')) and len(Hmax_re)-1>0:
        Hmax.append(Hmax_re.pop(len(Hmax_re)-1))
        Smax.append(Smax_re.pop(len(Smax_re)-1))
        Vmax.append(Vmax_re.pop(len(Vmax_re)-1))
        Hmin.append(Hmin_re.pop(len(Hmin_re)-1))
        Smin.append(Smin_re.pop(len(Smin_re)-1))
        Vmin.append(Vmin_re.pop(len(Vmin_re)-1))
        setpos()
        print("max")
        print(Hmax[len(Hmax)-1],Smax[len(Smax)-1],Vmax[len(Vmax)-1])
        print("min")
        print(Hmin[len(Hmin)-1],Smin[len(Smin)-1],Vmin[len(Vmin)-1])
cv2.destroyAllWindows()









