import math
import numpy as np 
import transformations as tf 
import sched, time

class Knot:
	
	origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
	p1 = 0.9808
	p2 = 0.8315
	p3 = 0.5556
	p4 = 0.1951

	#set properties
	tilt = 15.0
	bendRad = 2.0
	pipeRad = 0.8
	tilttan = math.tan(math.radians(tilt))

	b0 = [p1*pipeRad,p4*pipeRad,0]
	b1 = [p2*pipeRad,p3*pipeRad,0]
	b2 = [p3*pipeRad,p2*pipeRad,0]
	b3 = [p4*pipeRad,p1*pipeRad,0]

	b4 = [-p4*pipeRad,p1*pipeRad,0]
	b5 = [-p3*pipeRad,p2*pipeRad,0]
	b6 = [-p2*pipeRad,p3*pipeRad,0]
	b7 = [-p1*pipeRad,p4*pipeRad,0]
	b8 = [-p1*pipeRad,-p4*pipeRad,0]
	b9 = [-p2*pipeRad,-p3*pipeRad,0]
	b10 = [-p3*pipeRad,-p2*pipeRad,0]
	b11 = [-p4*pipeRad,-p1*pipeRad,0]

	b12 = [p4*pipeRad,-p1*pipeRad,0]
	b13 = [p3*pipeRad,-p2*pipeRad,0]
	b14 = [p2*pipeRad,-p3*pipeRad,0]
	b15 = [p1*pipeRad,-p4*pipeRad,0]

	m0 = [p1*pipeRad,p4*pipeRad,(bendRad-p1*pipeRad)*tilttan]
	m1 = [p2*pipeRad,p3*pipeRad,(bendRad-p2*pipeRad)*tilttan]
	m2 = [p3*pipeRad,p2*pipeRad,(bendRad-p3*pipeRad)*tilttan]
	m3 = [p4*pipeRad,p1*pipeRad,(bendRad-p4*pipeRad)*tilttan]

	m4 = [-p4*pipeRad,p1*pipeRad,(bendRad+p4*pipeRad)*tilttan]
	m5 = [-p3*pipeRad,p2*pipeRad,(bendRad+p3*pipeRad)*tilttan]
	m6 = [-p2*pipeRad,p3*pipeRad,(bendRad+p2*pipeRad)*tilttan]
	m7 = [-p1*pipeRad,p4*pipeRad,(bendRad+p1*pipeRad)*tilttan]

	m8 = [-p1*pipeRad,-p4*pipeRad,(bendRad+p1*pipeRad)*tilttan]
	m9 = [-p2*pipeRad,-p3*pipeRad,(bendRad+p2*pipeRad)*tilttan]
	m10 = [-p3*pipeRad,-p2*pipeRad,(bendRad+p3*pipeRad)*tilttan]
	m11 = [-p4*pipeRad,-p1*pipeRad,(bendRad+p4*pipeRad)*tilttan]

	m12 = [p4*pipeRad,-p1*pipeRad,(bendRad-p4*pipeRad)*tilttan]
	m13 = [p3*pipeRad,-p2*pipeRad,(bendRad-p3*pipeRad)*tilttan]
	m14 = [p2*pipeRad,-p3*pipeRad,(bendRad-p2*pipeRad)*tilttan]
	m15 = [p1*pipeRad,-p4*pipeRad,(bendRad-p1*pipeRad)*tilttan]
	blist = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15]
	mlist = [m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15]

	# azims = [0,0,0,-45.0,0]
	utx = -55
	uty = 0
	utz = 0
	ux = -3.34
	uy = 0
	uz = 0
	azimStep = 0.001

	def __init__(self):
		self.modules = []
		self.azims = []
		# for trefoil, this is array of 3 points
		self.end1a = []
		self.end1b = []
		self.end2a = []
		self.end2b = []
		self.optimizing = False
		self.sigma = 1
		self.currCost = 0
		self.s = None
		self.symmetry = True
		self.length = 0
		self.trefoil = False

 	'''Knot Building Section '''

	def buildKnot(self,azims,symmetry=False):
		del self.modules[:]
		self.azims = azims
		self.symmetry = symmetry
		if symmetry:
			for i in range(len(self.azims)):
				self.modules.append(self.module(i))
				self.modules.append(self.module(i,False))
			self.modules.append(self.buildBase())
			# print "dis",self.endDistance()
			# print "ang",self.endAngle()
			# print self.currCost
		else:
			for i in range(len(self.azims)):
				if i < len(self.azims)/2:
					self.modules.append(self.module(i))
				else:
					j = i%(len(self.azims)/2)
					self.modules.append(self.module(j,False))
			self.modules.append(self.buildBase())
		# self.length = self.wormLength()

	def buildTrefoil(self,azims):
		self.trefoil = True
		del self.modules[:]
		del self.end1a[:]
		del self.end1b[:]
		del self.end2b[:]
		del self.end2a[:]
		
		self.azims = azims
		#first lobe
		self.buildLobe(None)
		#second lobe
		self.buildLobe(120)
		#third lobe
		self.buildLobe(-120)

	def buildLobe(self,rotation=None):
		for i in range(len(self.azims)):
			upper = self.module(i,rotations=[Knot.utx,Knot.uty,Knot.utz],translations=[Knot.ux,Knot.uy,Knot.uz],lobe_rotation=rotation)
			lower = self.module(i,upper=False,rotations=[Knot.utx,Knot.uty,Knot.utz],translations=[Knot.ux,Knot.uy,Knot.uz],lobe_rotation=rotation)
			self.modules.append(upper)
			self.modules.append(lower)
		base = self.buildBase()
		base = np.dot(base,tf.rotation_matrix(math.radians(Knot.utx),[1,0,0])[:3,:3].T)
		base = np.dot(base,tf.rotation_matrix(math.radians(Knot.uty),[0,1,0])[:3,:3].T)
		base = np.dot(base,tf.rotation_matrix(math.radians(Knot.utz),[0,0,1])[:3,:3].T)
		base = base + np.array([Knot.ux,Knot.uy,Knot.uz])
		if rotation:
			base = np.dot(base,tf.rotation_matrix(math.radians(rotation),[0,1,0])[:3,:3].T)
		self.modules.append(base)


	def module(self,numRotations,upper=True,rotations=None,translations=None,lobe_rotation=None):
		numRotations +=1
		m = 2
		points = np.array(Knot.mlist+Knot.blist)
		pointFlipped = self.flipped(points)
		rotated = points
		rFlipped = pointFlipped
		azims = self.azims
		if upper == False:
			if self.symmetry:
				azims = [-a for a in self.azims]
			m = -2
			# need extra rotation for lower half
			rotated = rotated - np.array([Knot.bendRad,0,0])
			rotated = np.dot(rotated,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
			rotated = rotated + np.array([Knot.bendRad,0,0])

			rFlipped= rFlipped - np.array([Knot.bendRad,0,0])
			rFlipped = np.dot(rFlipped,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
			rFlipped = rFlipped + np.array([Knot.bendRad,0,0])
		# print numRotations
		for i in range(numRotations):
			aIndex = numRotations - i - 1
			if self.symmetry == False and upper == False:
				aIndex += len(self.azims)/2 
			rotated = np.dot(rotated,tf.rotation_matrix(math.radians(azims[aIndex]),[0,0,1])[:3,:3].T)
			rFlipped = np.dot(rFlipped,tf.rotation_matrix(math.radians(azims[aIndex]),[0,0,1])[:3,:3].T)
			if aIndex != 0:
				rotated = rotated - np.array([Knot.bendRad,0,0])
				rotated = np.dot(rotated,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
				rotated = rotated + np.array([Knot.bendRad,0,0])

				rFlipped= rFlipped - np.array([Knot.bendRad,0,0])
				rFlipped = np.dot(rFlipped,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
				rFlipped = rFlipped + np.array([Knot.bendRad,0,0])
		
		if upper == False and self.symmetry == True:
			m = -1
		else: m = 1
		#half rotation for upper and lower so base module fits in between
		rotated = rotated - np.array([Knot.bendRad,0,0])
		rotated = np.dot(rotated,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		rotated = rotated + np.array([Knot.bendRad,0,0])

		rFlipped= rFlipped - np.array([Knot.bendRad,0,0])
		rFlipped = np.dot(rFlipped,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		rFlipped = rFlipped + np.array([Knot.bendRad,0,0])

		if rotations:
			rotated = np.dot(rotated,tf.rotation_matrix(math.radians(rotations[0]),[1,0,0])[:3,:3].T)
			rotated = np.dot(rotated,tf.rotation_matrix(math.radians(rotations[1]),[0,1,0])[:3,:3].T)
			rotated = np.dot(rotated,tf.rotation_matrix(math.radians(rotations[2]),[0,0,1])[:3,:3].T)

			rFlipped = np.dot(rFlipped,tf.rotation_matrix(math.radians(rotations[0]),[1,0,0])[:3,:3].T)
			rFlipped = np.dot(rFlipped,tf.rotation_matrix(math.radians(rotations[1]),[0,1,0])[:3,:3].T)
			rFlipped = np.dot(rFlipped,tf.rotation_matrix(math.radians(rotations[2]),[0,0,1])[:3,:3].T)

		if translations:
			rotated = rotated + np.array(translations)
			rFlipped = rFlipped + np.array(translations)

		if lobe_rotation:
			rotated = np.dot(rotated,tf.rotation_matrix(math.radians(lobe_rotation),[0,1,0])[:3,:3].T)
			rFlipped = np.dot(rFlipped,tf.rotation_matrix(math.radians(lobe_rotation),[0,1,0])[:3,:3].T)

		#if end module, compute center of blist and center of all points
		isEnd = False
		if self.symmetry:
			isEnd = (numRotations-1) == (len(self.azims)-1)
		else:
			isEnd = (numRotations-1) == (len(self.azims)/2 - 1)
		if isEnd:
			
			
			if upper:
				x_bar = sum([r[0] for r in rFlipped])/len(rFlipped)
				y_bar = sum([r[1] for r in rFlipped])/len(rFlipped)
				z_bar = sum([r[2] for r in rFlipped])/len(rFlipped)
				if self.trefoil:
					self.end1a.append(np.array([x_bar,y_bar,z_bar]))
				else:
					self.end1a = np.array([x_bar,y_bar,z_bar])
				b = rFlipped[rFlipped.shape[0]/2:]
				b_x_bar = sum([r[0] for r in b])/len(b)
				b_y_bar = sum([r[1] for r in b])/len(b)
				b_z_bar = sum([r[2] for r in b])/len(b)
				if self.trefoil:
					self.end1b.append(np.array([b_x_bar,b_y_bar,b_z_bar]))
				else:
					self.end1b = np.array([b_x_bar,b_y_bar,b_z_bar])
			else:
				x_bar = sum([r[0] for r in rotated])/len(rotated)
				y_bar = sum([r[1] for r in rotated])/len(rotated)
				z_bar = sum([r[2] for r in rotated])/len(rotated)
				if self.trefoil:
					self.end2a.append(np.array([x_bar,y_bar,z_bar]))
				else:
					self.end2a = np.array([x_bar,y_bar,z_bar])
				b = rotated[rotated.shape[0]/2:]
				b_x_bar = sum([r[0] for r in b])/len(b)
				b_y_bar = sum([r[1] for r in b])/len(b)
				b_z_bar = sum([r[2] for r in b])/len(b)
				if self.trefoil:
					self.end2b.append(np.array([b_x_bar,b_y_bar,b_z_bar]))
				else:
					self.end2b = np.array([b_x_bar,b_y_bar,b_z_bar])

		return rotated, rFlipped

	def buildBase(self):
		points = np.array(Knot.mlist+Knot.blist)
		pointFlipped = self.flipped(points)
		rotated = points
		rFlipped = pointFlipped
		rotated = rotated - np.array([Knot.bendRad,0,0])
		rotated = np.dot(rotated,tf.rotation_matrix(-1*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		rotated = rotated + np.array([Knot.bendRad,0,0])

		rFlipped= rFlipped - np.array([Knot.bendRad,0,0])
		rFlipped = np.dot(rFlipped,tf.rotation_matrix(-1*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		rFlipped = rFlipped + np.array([Knot.bendRad,0,0])
		return rotated,rFlipped

	'''Optimization Section'''
	def startOptimizing(self):
		print "starting optimization"
		if not self.optimizing:
			self.optimizing = True
			self.s = sched.scheduler(time.time,time.sleep)
			self.s.enter(0.001,1,self.optimize,())
			self.s.run()

	def stopOptimizing(self):
		print "stopping optimization"
		if self.optimizing:
			self.optimizing = False
			self.s = None

	def setSigma(self,num):
		self.sigma = num
		print "set sigma to ",self.sigma

	def cost(self):
		angleFactor = 100
		# if self.endDistance() < 0.35:
			# angleFactor = 10
		# angle = max(self.endAngle()/(self.endDistance()*angleFactor), 0.2)
		# distance = self.endDistance()
		# print "angle portion ", angle
		# print "distance portion ", distance
		# return angle,distance,angle + distance
		return 0,0,0

	def optimize(self):
		# if self.optimizing:
		increments = []
		betas = []
		gammas = []
		# time1 = time.time()
		for i in range(len(self.azims)):
			increments.append(self.takeAzimuthStep(i))
			betas.append(self.takeBetaStep(i))
			gammas.append(self.takeGammaStep(i))
		print increments
		print betas
		print gammas
		# time2 = time.time()
		arr = [abs(x) for x in increments+betas+gammas]
		biggest = float(max(arr))
		biggestArr = []
		ind = arr.index(biggest)
		if ind < 16:
			biggestArr = increments
		elif ind >= 16 and ind < 32:
			biggestArr = betas
		else:
			biggestArr = gammas
		# for i in range(len(self.azims)):
		# 	biggestArr[i] = biggestArr[i]/biggest * Knot.azimStep
			# increments[i] = increments[i]/biggest * Knot.azimStep			
			# betas[i] = betas[i]/biggest * Knot.azimStep
			# gammas[i] = gammas[i]/biggest * Knot.azimStep
		# time3 = time.time()
		if biggestArr == increments:
			for i in range(len(self.azims)):
				self.azims[i] += (biggestArr[i]/biggest)*Knot.azimStep*self.sigma
		elif biggestArr == betas:
			i = 16-32+ind
			print "ind ",ind
			print "i ",i
			self.updateAzimsForBeta(i, biggest, biggestArr)
		elif biggestArr == gammas:
			i = -32+ind
			print "ind ",ind
			print "i ", i
			self.updateAzimsForGamma(i, biggest, biggestArr)
		# self.azims[i] += (increments[i]+betas[i]+gammas[i])*self.sigma
		# time4 = time.time()
		print "azims ",self.azims
		self.buildKnot(self.azims)
		# time5 = time.time()
		self.currCost = self.cost()[2]
		print "angle cost: ", self.cost()[0], " distance cost ",self.cost()[1]," total ",self.currCost
		print "angle",self.endAngle()
		print "distance",self.endDistance()
		# print time2-time1
		# print time3-time2
		# print time4-time3
		# print time5-time4
		# self.s.enter(0.1,1,self.optimize,())

	def updateAzimsForGamma(self,i, biggest, biggestArr):
		print biggestArr
		res = [0]*len(self.azims)
		j = i
		# change everything <= i
		while (j >= 1):
			ratioFactor = biggestArr[j]/biggest
			increment = ratioFactor * self.sigma * Knot.azimStep
			self.azims[j-1] += increment
			self.azims[j] -= 2*increment
			self.azims[j+1] += increment
			res[j-1] = increment
			res[j] = 2*increment
			res[j+1] = increment
			j -= 3
		# change everything > i
		j = i+3
		while (j < len(biggestArr)-1):
			ratioFactor = biggestArr[j]/biggest
			increment = ratioFactor * self.sigma * Knot.azimStep
			self.azims[j-1] += increment
			self.azims[j] -= 2*increment
			self.azims[j+1] += increment
			res[j-1] = increment
			res[j] = 2*increment
			res[j+1] = increment
			j += 3
		print res

	def updateAzimsForBeta(self, i, biggest, biggestArr):
		res = [0]*len(self.azims)
		j = i
		# change everything <= i
		while (j >= 0):
			ratioFactor = biggestArr[j]/biggest
			increment = ratioFactor * self.sigma * Knot.azimStep
			self.azims[j] += increment
			self.azims[j+1] -= increment
			res[j] = increment
			res[j+1] = increment
			j -= 2
		# change everything > i
		j = i+2
		while (j < len(biggestArr)-1):
			ratioFactor = biggestArr[j]/biggest
			increment = ratioFactor * self.sigma * Knot.azimStep
			self.azims[j] += increment
			self.azims[j+1] -= increment
			res[j] = increment
			res[j+1] = increment
			j += 2
		print res

	'''Helpers'''

	def printStats(self):
		print "azims ",self.azims
		print "angle cost: ", self.cost()[0], " distance cost ",self.cost()[1]," total ",self.currCost
		print "angle",self.endAngle()
		print "distance",self.endDistance()

	def endDistance(self):
		if self.trefoil:
			end1 = self.end1a[0]
			end2 = self.end2a[2]
			return math.sqrt((end1[0]-end2[0])**2 + (end1[1]-end2[1])**2 + (end1[2]-end2[2])**2)
		return math.sqrt((self.end1b[0]-self.end2b[0])**2 + (self.end1b[1]-self.end2b[1])**2 + (self.end1b[2]-self.end2b[2])**2)

	def endMidDistance(self):
		return math.sqrt((self.end1a[0]-self.end2a[0])**2 + (self.end1a[1]-self.end2a[1])**2 + (self.end1a[2]-self.end2a[2])**2)

	def endAngle(self):
		if self.trefoil:
			v1 = self.end1b[0] - self.end1a[0]
			v2 = self.end2b[2] - self.end2a[2]
		else:
			v1 = self.end1b - self.end1a
			v2 = self.end2b - self.end2a
		# print math.degrees(tf.angle_between_vectors(v1,v2))
		return 180-math.degrees(tf.angle_between_vectors(v1,v2))

	def takeAzimuthStep(self,i):
		azim = self.azims[i]
		astep = azim+Knot.azimStep
		temp = self.azims
		temp[i] = astep
		if self.trefoil:
			self.buildTrefoil(temp)
		else:
			self.buildKnot(temp)
		# print "the cost with a 0.001 change in the",i," is ", str(self.cost())
		# print "the improvement is " +str(self.currCost-self.cost())
		# print ""	
		improvementRatio = (self.currCost-self.cost()[2]) / self.currCost
		# print "improvement ratio: ",improvementRatio
		aIncrement = improvementRatio
		# print "a",i," incremenet: ",aIncrement
		# print ""
		return aIncrement

	def takeBetaStep(self,i):
		if i < len(self.azims) - 1:
			azim = self.azims[i]
			astep = azim+Knot.azimStep
			temp = self.azims
			temp[i] = astep
			azim2 = self.azims[i+1]
			a2step = azim2 - Knot.azimStep
			temp[i+1] = a2step
			azim = self.azims[i]
			if self.trefoil:
				self.buildTrefoil(temp)
			else:
				self.buildKnot(temp)
			# print "the cost with a 0.001 change in the",i," is ", str(self.cost())
			# print "the improvement is " +str(self.currCost-self.cost())
			# print ""
			improvementRatio = (self.currCost-self.cost()[2]) / self.currCost
			# print "improvement ratio: ",improvementRatio
			aIncrement = improvementRatio
			# print "a",i," incremenet: ",aIncrement
			# print ""
			return aIncrement
		return 0

	def takeGammaStep(self,i):
		if i > 0 and i < len(self.azims)-1:
			azim = self.azims[i]
			astep = azim-2*Knot.azimStep
			temp = self.azims
			temp[i] = astep
			azim2 = self.azims[i-1]
			a2Step = azim2 + Knot.azimStep
			temp[i-1] = a2Step
			azim3 = self.azims[i+1]
			a3Step = azim3 + Knot.azimStep
			temp[i+1] = a3Step
			if self.trefoil:
				self.buildTrefoil(temp)
			else:
				self.buildKnot(temp)
			# print "the cost with a 0.001 change in the",i," is ", str(self.cost())
			# print "the improvement is " +str(self.currCost-self.cost())
			# print ""
			improvementRatio = (self.currCost-self.cost()[2]) / self.currCost
			# print "improvement ratio: ",improvementRatio
			aIncrement = improvementRatio
			# print "a",i," incremenet: ",aIncrement
			# print ""
			return aIncrement
		return 0

	def flipped(self,points):
		#rotate 180
		rotated = np.dot(points,tf.rotation_matrix(math.pi,[1,0,0])[:3,:3].T)
		#translate out bend rad
		rotated = rotated - np.array([Knot.bendRad,0,0])
		#tilt
		rotated = np.dot(rotated,tf.rotation_matrix(2*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		#translate back
		rotated = rotated + np.array([Knot.bendRad,0,0])
		return rotated

	def wormLength(self):
		segment = math.sqrt((self.end1a[0]-self.end1b[0])**2 + (self.end1a[1]-self.end1b[1])**2 + (self.end1a[2]-self.end1b[2])**2)
		return segment*4*len(self.modules)

