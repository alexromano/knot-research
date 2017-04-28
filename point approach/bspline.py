import scipy
import numpy as np
import pylab as plt 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import scipy.interpolate as si


#NEED ANOTHER POINT ON THE OTHER SIDE OF X AXIS (X, -Y, -Z)
def Bspline(plist,numPoints=128):
	#point list:
	# last = [plist[-3],plist[-2],plist[-1]] #last three points
	# plist = np.concatenate((last,plist))
	plist = np.array(plist)

	#x,y,z control points:
	x = plist[:,0]
	y = plist[:,1]
	z = plist[:,2]

	#knot vectors:

	l = len(x)

	t = np.linspace(0,1,l-2, endpoint = True)
	t = np.append([0,0,0],t)
	t = np.append(t,[1,1,1])	

	tck = [t,[x,y,z],3]
	u3 = np.linspace(0,1,(max(l*2,numPoints)),endpoint = True)
	out = np.array(si.splev(u3,tck))
	out = out.T

	# need to remove outside points for some reason
	j = numPoints/13
	out = out[j:-j]

	return out

def CatmullRomSpline(P0,P1,P2,P3,nPoints=100):
	'''
	P0, P1, P2, and P3 should be (x,y,z) points that define the Bspline.
	nPoints is the number of points to include on this curve segment.
	'''

	P0,P1,P2,P3 = map(np.array,[P0,P1,P2,P3])

	# Calculate t0 to t4
	alpha = 0.5
	def tj(ti, Pi, Pj):
		xi, yi, zi = Pi
		xj, yj, zj = Pj
		return ( ( (xj-xi)**2 + (yj-yi)**2 + (zj-zi)**2)**0.5 )**alpha + ti

	t0 = 0
	t1 = tj(t0, P0, P1)
	t2 = tj(t1, P1, P2)
	t3 = tj(t2, P2, P3)

	# Only calculate points between P1 and P2
	t = np.linspace(t1,t2,nPoints)

	# Reshape so that we can multiply by the points P0 to P3
	# and get a point for each value of t.
	t = t.reshape(len(t),1)

	A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
	A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
	A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

	B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
	B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

	C  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
	return C

def CatmullRomChain(P):
	"""
	Calculate Catmull Rom for a chain of points and return the combined curve.
	"""
	sz = len(P)

	# The curve C will contain an array of (x,y) points.
	C = []
	for i in range(sz-3):
		c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3])
		C.extend(c)

	return C

# Define a set of points for curve to go through
Points = [[10.0, -2.0, 4.0],
[-6.732, 7.66, -4.0],
[-6.732, -7.66, 4.0],
[10.0, 2.0, -4.0],
[-3.268,  9.66, 4.0],
[-3.268,  -9.66, -4.0],
[10.0, -2.0, 4.0],
[-6.732, 7.66, -4.0],
[-6.732, -7.66, 4.0]]

# Calculate the Catmull-Rom splines through the points
c = CatmullRomChain(Points)

p = np.array(Points)
p = p.transpose()
# Convert the Catmull-Rom curve points into x,y,z arrays and plot
# x,y,z = zip(*c)
# fig = plt.figure()
# ax = Axes3D(fig)
# ax.plot(p[0], p[1], p[2], label='originalpoints', lw =2, c='Dodgerblue')
# ax.plot(x,y,z, label='fit', lw =2, c='red')
# ax.legend()
# plt.savefig('junk.png')
# plt.show()

# #now lets plot it!
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = Axes3D(fig)
# # ax.plot(data[0], data[1], data[2], label='originalpoints', lw =2, c='Dodgerblue')
# ax.plot(new[0], new[1], new[2], label='fit', lw =2, c='red')
# ax.legend()
# plt.savefig('junk.png')
# plt.show()