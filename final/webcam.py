import cv2
from threading import Thread

class Webcam:

	def __init__(self):
		self.video_capture = cv2.VideoCapture(0)
		self.current_frame = self.video_capture.read()[1]
		print 'Video resolution: '+' x '.join(self.set_res(self.video_capture,1520,820))

	# create thread for capturing images
	def start(self):
		Thread(target=self._update_frame, args=()).start()

	def _update_frame(self):
		while(True):
			self.current_frame = self.video_capture.read()[1]

	# get the current frame
	def get_current_frame(self):
		return self.current_frame

	def set_res(self, cap, x,y):
		cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, int(x))
		cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, int(y))
		return str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
