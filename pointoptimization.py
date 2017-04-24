import bspline
import numpy as np
from scipy.spatial.distance import pdist
import transformations as tf
import math

class Knot:

	STEPSIZE = 	0.001

	def __init__(self,controlPoints,numSamples=30):
		# Calculate the Bspline with the control points
		interp = bspline.Bspline(controlPoints)
		print "taking " + str(numSamples) + " samples from " + str(len(interp)) + " points"
		self.numSamples = numSamples
		i = len(interp)/numSamples
		points = interp[::i]
		self.points = points[5*len(points)/6-1:6*len(points)/6-2]
		self.currCost = 0
		self.SIGMA = 1.0

	'''Optimization Section'''
	def cost(self,points):

		distanceStd = self.distanceStd(points)
		angleDev = self.angleDev(points)
		# separationDev = self.separationDev(points)

		return distanceStd + 10*angleDev #+ (separationDev**2)

	def takeStep(self,coord,i):
		point = self.points[i]
		pointPlus = []
		pointMinus = []
		if coord == 'x':
			pointPlus = np.array([point[0]+Knot.STEPSIZE, point[1],point[2]])
			pointMinus = np.array([point[0]-Knot.STEPSIZE, point[1],point[2]])
		elif coord == 'y':
			pointPlus = np.array([point[0], point[1]+Knot.STEPSIZE,point[2]])
			pointMinus = np.array([point[0], point[1]-Knot.STEPSIZE,point[2]])
		elif coord == 'z':
			pointPlus = np.array([point[0], point[1],point[2]+Knot.STEPSIZE])
			pointMinus = np.array([point[0], point[1],point[2]-Knot.STEPSIZE])
		temp = self.points.copy()
		# temp2 = self.points.copy()
		temp[i] = pointPlus
		# temp2[i] = pointMinus
		#re compute cost with this step
		newCost = self.cost(temp)
		# newCost = (self.cost(temp) - self.cost(temp2)) / (2 * Knot.STEPSIZE)
		#try costPlus - costMinus / 2 * stepsize
		#determine difference from previous cost and return improvement ratio
		improvementRatio = (self.currCost-newCost) / self.currCost
		return improvementRatio

	def optimize(self):
		print self.points
		while self.currCost > 0.086:
			increments = []
			plus = 0
			minus = 0
			for i in range(0,len(self.points)):
				x = self.takeStep('x',i)
				if x > 0:
					plus = plus + 1
				else: 
					minus = minus + 1
				y = self.takeStep('y',i)
				if y > 0:
					plus = plus + 1
				else: 
					minus = minus + 1
				z = self.takeStep('z',i)
				if z > 0:
					plus = plus + 1
				else: 
					minus = minus + 1
				increments.append([x,y,z])

			inc = np.array(increments)
			# biggestX = float(max(inc[:,0]))
			# biggestY = float(max(inc[:,1]))
			# biggestZ = float(max(inc[:,2]))
			# ind = increments.index(biggest)
			for i in range(len(increments)):
				# incPoints = np.array([inc[i,0]/biggestX,inc[i,1]/biggestY,inc[i,2]/biggestZ])
				self.points[i] += inc[i]*Knot.STEPSIZE*self.SIGMA

			#recompute cost
			newCost = self.cost(self.points)
			
			self.currCost = newCost
			print "plus ", plus
			print "minus ", minus
			print "new cost ",newCost

	'''Helpers'''

	def setSigma(self,val):
		self.SIGMA = val
		print "set SIGMA to ",val

	def angleDev(self,points):
		#calculate "kink" angles between segments
		cosines = []
		for i in range(len(points)):
			p1 = None
			p2 = None
			p3 = None
			if i == 0:
				nbr = points[1]
				reflected = np.dot(nbr, tf.rotation_matrix(math.pi,points[i],[0,0,0])[:3,:3].T)
				p1 = reflected
				p2 = points[i]
				p3 = points[i+1]
			elif i == len(points)-1:
				nbr = points[len(points)-2]
				reflected = np.dot(nbr, tf.rotation_matrix(math.pi,points[i],[0,0,0])[:3,:3].T)
				p1 = points[i-1]
				p2 = points[i]
				p3 = reflected
			else:
				p1 = points[i-1]
				p2 = points[i]
				p3 = points[i+1]
			v1 = p2-p1
			v2 = p3-p2
			angle_rads = tf.angle_between_vectors(v1,v2)
			cosines.append(math.cos(angle_rads))
		#degrees? radians? check.q
		dev = np.average(((np.array(cosines) - math.cos(0.5236))**2))
		# angleDev = np.sqrt(np.average((np.cos(np.array(angles))-math.cos(30))**2))

		print "cosines ", cosines[0:3]
		print "angle dev ", dev

		return dev


	def distanceStd(self,points):
		#calculate distances between neighboring segments
		distances = []	
		for i in range(len(points)):
			if i == 0:
				# relfect next point over this axis
				nbr = points[1]
				reflected = np.dot(nbr, tf.rotation_matrix(math.pi,points[i],[0,0,0])[:3,:3].T)
				distances.append(np.linalg.norm(points[i]-reflected))
			elif i == len(points)-1:
				# reflect previous point over this axis
				nbr = points[len(points)-2]
				print nbr
				reflected = np.dot(nbr, tf.rotation_matrix(math.pi,points[i],[0,0,0])[:3,:3].T)
				print reflected
				distances.append(np.linalg.norm(points[i]-reflected))
			else:
				distances.append(np.linalg.norm(points[i]-points[i+1]))
		dstd = np.std(distances)
		print "distances ",distances[0:3]
		print "std ", dstd
		return dstd


	def separationDev(self,points, diameter=2.0):
		# calculate separation of points from eachother (other than neighbors)
		# can't use symmetry)
		separations = []
		#build whole knot
		c = points
		c2 = np.dot(c, tf.rotation_matrix(math.pi,c[0],[0,0,0])[:3,:3].T)
		c2 = np.array(c2[::-1])
		c = np.concatenate((c2[0:len(c2)-1],c))
		
		rotated1 = np.dot(c, tf.rotation_matrix(math.radians(-120),[0,0,1])[:3,:3].T)
		rotated1 = rotated1[1:]
		rotated2 = np.dot(c, tf.rotation_matrix(math.radians(120),[0,0,1])[:3,:3].T)
		rotated2 = rotated2[1:]
		c = np.concatenate((c,rotated1))
		c = np.concatenate((c,rotated2))
		c = c[1:]

		# find pairwise distances (except neighbors)
		for i in range(len(points)):
			for j in range(len(points)):
				if i == j:
					continue
				if i == 0:
					if j == len(points)-1 or j == 1:
						continue
				elif i == len(points)-1:
					if j == 0 or j == len(points) - 2:
						continue
				else:
					if j == i+1 or j == i - 1:
						continue
				separations.append(np.linalg.norm(points[i]-points[j]))
		dev = np.average(((np.array(separations) - (diameter*1.2))**2))

		print "separations ", separations[0:3]
		print "separation dev ", dev

		return dev






