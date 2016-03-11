import cv2
import numpy as np
from matplotlib import pyplot as plt

def run_main():
	imgg = cv2.imread('IMG_20160120_132852_img_6.png',cv2.IMREAD_GRAYSCALE)
	surf = cv2.SURF()
	kp, descritors = surf.detectAndCompute(imgg,None,useProvidedKeypoints = False)
	
	
	# Setting up samples and responses for kNN
	samples = np.array(descritors)
	responses = np.arange(len(kp),dtype = np.float32)
	# kNN training
	knn = cv2.KNearest()
	knn.train(samples,responses)
	
	# Now loading a template image and searching for similar keypoints
	templateg = cv2.imread('IMG_20160120_133913_img_5.png',cv2.IMREAD_GRAYSCALE)
	keys,desc = surf.detectAndCompute(templateg,None,useProvidedKeypoints = False)
	for h,des in enumerate(desc):
		des = np.array(des,np.float32).reshape(1, len(des))
		retval, results, neigh_resp, dists = knn.find_nearest(des,1)
		res,dist =  int(results[0][0]),dists[0][0]

		if dist<0.1: # draw matched keypoints in red color
			color = (0,0,255)
		else:  # draw unmatched in blue color
			print dist
			color = (255,0,0)

		#Draw matched key points on original image
		x,y = kp[res].pt
		center = (int(x),int(y))
		cv2.circle(imgg,center,2,color,-1)

		#Draw matched key points on template image
		x,y = keys[h].pt
		center = (int(x),int(y))
		cv2.circle(templateg,center,2,color,-1)

	cv2.imshow('img',imgg)
	cv2.imshow('tm',templateg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return 0

if __name__ == "__main__":
	run_main()