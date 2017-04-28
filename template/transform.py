import numpy as np
import math

upVec = np.array([0,0,1])
eyeVec = np.array([0,10,10])

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: 
       return v
    return v/norm

def rotate(degrees,axis):
	x = axis[0]
	y = axis[1]
	z = axis[2]

	cos_theta = math.cos(math.radians(degrees))
	sin_theta = math.sin(math.radians(degrees))

	I = np.eye(3)

	t_product = np.array([[x*x,x*y,x*z],[y*x,y*y,y*z],[z*x,z*y,z*z]])
	# print t_product
	c_product = np.array([[0.0,-z,y],[z,0.0,-x],[-y,x,0.0]])

	return I*cos_theta + (1.0 - cos_theta)*t_product + sin_theta*c_product

def left(degrees,eye,up):
	# print eye
	eyeVec = np.dot(rotate(degrees,up),eye)
	# print eyeVec
	return eyeVec

def up(degrees,eye,up):
	orth = normalize(np.cross(eye,up))
	# print eye
	# print up
	# print orth
	rotMat = rotate(-degrees,orth)
	eyeVec = np.dot(rotMat,eye)

	upVec = normalize(np.dot(rotMat,up))

	return eyeVec, upVec

def lookAt(eye,up):
	w = normalize(eyeVec)
	u = normalize(np.cross(upVec,w))
	v = normalize(np.cross(w,u))
	return np.array([[u[0],u[1],u[2],-u[0]*eyeVec[0] - u[1]*eyeVec[1] - u[2]*eyeVec[2]],
		[v[0],v[1],u[2],-v[0]*eyeVec[0] - v[1]*eyeVec[1] - v[2]*eyeVec[2]],
		[w[0],w[1],u[2],-w[0]*eyeVec[0] - w[1]*eyeVec[1] - w[2]*eyeVec[2]],
		[0,0,0,1.0]])