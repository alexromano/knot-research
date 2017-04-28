import math
import numpy as np 
import transformations as tf 

class Geometry:

	origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)

	'''
	Define some initial points here
	I made a cube for now but change this
	'''
	#Top face
	p1 = [1, 1, -1]
	p2 = [-1.0, 1.0, -1.0]
	p3 = [-1.0, 1.0,  1.0]
	p4 = [1.0, 1.0,  1.0]

	# Bottom face
	p5 = [1.0, -1.0,  1.0]
	p6 = [-1.0, -1.0,  1.0]
	p7 = [-1.0, -1.0, -1.0]
	p8 = [1.0, -1.0, -1.0]

	plist = [p1,p2,p3,p4,p5,p6,p7,p8]

	def __init__(self):
		self.cubes = []
		self.extraTranslation = 0

	'''Building Section'''

	def buildGeometry(self):
		del self.cubes[:]
		# make a few translated cubes
		for i in range(4):
			print "building cube", i
			self.cubes.append(self.buildCube(i*3))

	def buildCube(self,translation):
		points = np.array(Geometry.plist)
		# add the x translation to the points
		p = points+ np.array([translation+self.extraTranslation,0,0])
		return p



