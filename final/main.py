from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from playerlib import GameCtrler
from PIL import Image
import numpy as np
from webcam import Webcam
from scipy import linalg
from glyphs import *
from causallib import causalBox
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from objloader import *
 
class OpenGLGlyphs:
	# constants
	INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
								[-1.0,-1.0,-1.0,-1.0],
								[-1.0,-1.0,-1.0,-1.0],
								[ 1.0, 1.0, 1.0, 1.0]])
	

	
	def __init__(self):
		# initialise webcam and start thread
		self.webcam = Webcam()
		self.webcam.start()
		
		#initialise
		self.hBox = causalBox(winSize = 10)
		self.vBox = causalBox(winSize = 10)
		
		plyerName = ["John","Doe","Tommy","Emmanuel"]
		self.game = GameCtrler(plyerName)
		
		# initialise shapes
		self.dragon = None
		self.fly = None
		self.ele = None
		self.boat = None
		self.horse = None
		self.house = None
		self.juk = None

		# textures
		self.texture_background = None

	def _init_gl(self, Width, Height):
		# initialPosition = (0,0,0) 
		glClearColor(0.0, 0.0, 0.0, 0.0)
		glClearDepth(1.0)
		glDepthFunc(GL_LESS)
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_SMOOTH)
		
		# Projection matrix
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		fovy = 2*np.arctan(Height/1375.0)*180.0/np.pi
		gluPerspective(fovy, float(Width)/float(Height), 0.1, 1375.1)
		glViewport(0,0,Width,Height)
		glMatrixMode(GL_MODELVIEW)

		# assign shapes
		print "loading model 1/7"
		self.dragon = OBJ('Drgn9-6.obj')
		print "loading model 2/7"
		self.fly = OBJ('plane.obj')
		print "loading model 3/7"
		self.ele = OBJ('minion.obj')
		print "loading model 4/7"
		self.boat = OBJ('VikingShip.mtl.obj')
		print "loading model 5/7"
		self.horse = OBJ('Wooden_Toy_Truck.obj')
		print "loading model 6/7"
		self.house = OBJ('house_001.obj')
		print "loading model 7/7"
		self.juk = OBJ('Barrel_variation.obj')
		print "loading model done"

		# enable textures
		glEnable(GL_TEXTURE_2D)
		self.texture_background = glGenTextures(1)

	def _draw_scene(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		
		# get image from webcam
		image = self.webcam.get_current_frame()

		self._draw_background(image)
		
		# handle glyphs
		image = self._handle_glyphs(image)
		
		glutSwapBuffers()
		
	def _handle_glyphs(self, image):
		
		
		# attempt to detect glyphs
		glyphs = []

		try:
			glyphs = detect_glyph(image, self.hBox, self.vBox, self.game)
		except Exception as ex: 
			print(ex)

		if not glyphs: 
			return
			
		for glyph in glyphs:
		
			rvecs, tvecs, glyph_name = glyph
			# build view matrix
			rmtx = cv2.Rodrigues(rvecs)[0]
			view_matrix = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0]],
									[rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[1]],
									[rmtx[2][0],rmtx[2][1],rmtx[2][2],tvecs[2]],
									[0.0       ,0.0       ,0.0       ,1.0    ]])
			view_matrix =  view_matrix * self.INVERSE_MATRIX 
			view_matrix = np.transpose(view_matrix)
			
			# load view matrix and draw cube
			glPushMatrix()
			glLoadIdentity()
			glLoadMatrixd(view_matrix)
			if glyph_name == "B juk":
				glCallList(self.juk.gl_list)
			elif glyph_name == "R juk":
				glCallList(self.juk.gl_list)
			elif glyph_name == "B Phao":
				glCallList(self.house.gl_list)
			elif glyph_name == "R Phao":
				glCallList(self.house.gl_list)
			elif glyph_name == "B Horse":
				glCallList(self.horse.gl_list)
			elif glyph_name == "R Horse":
				glCallList(self.horse.gl_list)
			elif glyph_name == "B Boat":
				glCallList(self.boat.gl_list)
			elif glyph_name == "R Boat":
				glCallList(self.boat.gl_list)
			elif glyph_name == "B Ele":
				glCallList(self.ele.gl_list)
			elif glyph_name == "R Ele":
				glCallList(self.ele.gl_list)
			elif glyph_name == "B Fly":
				glCallList(self.fly.gl_list)
			elif glyph_name	== "R Fly":
				glCallList(self.fly.gl_list)
			elif glyph_name == "B T":
				glCallList(self.dragon.gl_list)
			elif glyph_name == "R T":
				glCallList(self.dragon.gl_list)				
			else:
				glCallList(self.dragon.gl_list)				
			glPopMatrix()

	def _draw_background(self, image):
	
		# convert image to OpenGL texture format
		bg_image = cv2.flip(image, 0)
		bg_image = Image.fromarray(bg_image)     
		ix = bg_image.size[0]
		iy = bg_image.size[1]
		bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)
		
		# create background texture
		glBindTexture(GL_TEXTURE_2D, self.texture_background)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)

		# draw background
		glBindTexture(GL_TEXTURE_2D, self.texture_background)
		glPushMatrix()
		glLoadIdentity()
		glTranslatef(-100,100,-1375)
		glBegin(GL_QUADS)
		i, j = 1520/2, 820/2
		glTexCoord2f(0.0, 1.0); glVertex3f(-i, -j, 0.0)
		glTexCoord2f(1.0, 1.0); glVertex3f( i, -j, 0.0)
		glTexCoord2f(1.0, 0.0); glVertex3f( i,  j, 0.0)
		glTexCoord2f(0.0, 0.0); glVertex3f(-i,  j, 0.0)
		glEnd()
		glPopMatrix()

	def main(self):
	
		width = 1520
		heigh = 820
		# setup and run OpenGL
		glutInit()
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		glutInitWindowSize(760, 410)
		glutInitWindowPosition(100, 100)
		self.window_id = glutCreateWindow("OpenGL Glyphs")
		glutDisplayFunc(self._draw_scene)
		glutIdleFunc(self._draw_scene)
		self._init_gl(width, heigh)
		glutMainLoop()

# run an instance of OpenGL Glyphs 
openGLGlyphs = OpenGLGlyphs()
openGLGlyphs.main()