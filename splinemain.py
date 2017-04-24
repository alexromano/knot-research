from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import transform
import transformations as tf
import numpy as np
import bspline
import pointoptimization as opt

eye = np.array([0.0,-30.0,6.5])
up = np.array([0.0,0.0,1.0])

prevX = 0
prevY = 0
r = 0

# Define a set of points for curve to go through
Points = [[10.0, -2.0, 4.0],
[-6.732, 7.66, -4.0],
[-6.732, -7.66, 4.0],
[10.0, 2.0, -4.0],
[-3.268, 9.66, 4.0],
[-3.268,  -9.66, -4.0],
[10.0, -2.0, 4.0],
[-6.732, 7.66, -4.0],
[-6.732, -7.66, 4.0]
]
Points = np.dot(Points, tf.rotation_matrix(math.radians(60),[0,0,1])[:3,:3].T)
p1 = np.array(Points[5])
p2 = np.array(Points[6])
p3 = np.array(Points[7])
mp1 = (p1+p2)/2
mp2 = (p2+p3)/2
p = np.array([mp1,p2,mp2])
# print np.linalg.norm(np.array(Points[0])-np.array(Points[1]))
# print np.linalg.norm(np.array(Points[1])-np.array(Points[2]))
# v1 = np.array(Points[1]) - np.array(Points[0])
# v2 = np.array(Points[1]) - np.array(Points[2])
# print math.degrees(tf.angle_between_vectors(v1,v2))

# p = Points[:4]
# rotated1 = np.dot(p, tf.rotation_matrix(math.radians(-120),[0,0,1])[:3,:3].T)
# rotated2 = np.dot(p, tf.rotation_matrix(math.radians(120),[0,0,1])[:3,:3].T)
# p = np.concatenate((p,rotated1))
# p = np.concatenate((p,rotated2))

knot = opt.Knot(Points)
original = []

def init():
	glClearColor(0.0, 0.0, 0.0, 1.0); # Set background color to black and opaque
	glClearDepth(1.0);                   # Set background depth to farthest
	glEnable(GL_DEPTH_TEST);   # Enable depth testing for z-culling
	glDepthFunc(GL_LEQUAL);    # Set the type of depth-test
	glShadeModel(GL_SMOOTH);   # Enable smooth shading
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);

def mainDisplay():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	# # gluLookAt(0,13,1.5,  0,0,0,  0,0,1)
	# mv = transform.lookAt(eye,up)
	# # mv = np.transpose(mv)
	gluLookAt(eye[0],eye[1],eye[2],  0,0,0,  up[0],up[1],up[2])
	glBegin(GL_LINES)
	# x axis
	glColor3f(1.0, 0.0, 0.0) 
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(30.0,0.0,0.0)
	# y axis
	glColor3f(0.0,1.0,0.0)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(0.0,30.0,0.0)
	# z axis
	glColor3f(0.0,0.0,1.0)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(0.0,0.0,30.0)

	glEnd()

	global knot
	global original

	# save original points
	if knot.currCost == 0:
		original = knot.points.copy()
		# knot.points[4] = np.array([5,5,5])
		knot.currCost = knot.cost(knot.points)
	# draw original points for reference
	# glBegin(GL_LINES)
	# glColor3f(1.0, 0.0, 0.0);
	# for i in range(len(original)-1):
	# 	# if i == len(original)-1:
	# 	# 	glVertex3fv(original[i])
	# 	# 	glVertex3fv(original[0])
	# 	# else:
	# 	glVertex3fv(original[i])
	# 	glVertex3fv(original[i+1])

	# glEnd()
	glBegin(GL_LINES)
	# drawing the control lines
	
	glColor3f(1.0, 1.0, 1.0)
	x = p
	for i in range(len(x)-1):
		glVertex3fv(x[i])
		glVertex3fv(x[i+1])
	glEnd()

	glBegin(GL_LINES)
	c = knot.points
	
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
	
	# xAnchor = (c[len(c)/2]+c[len(c)/2-1])/2
	# c[len(c)/2] = xAnchor
	# c = np.delete(c,len(c)/2-1,0)
	# print(c)	
	# print("")
	# glVertex3fv(c[len(c)/2])
	# glVertex3fv(c[len(c)/2-1])
	for i in range(len(c)):
		if i == len(c)-1:
			glVertex3fv(c[i])
			glVertex3fv(c[0])
		else:
			glVertex3fv(c[i])
			glVertex3fv(c[i+1])
	glEnd()

	# glBegin(GL_POINTS)
	# glColor3f(1.0, 0.0, 0.0)
	# for i in range(len(c)):
	# 	glVertex3fv(c[i])
	# glEnd()
	# knot.distanceStd(c)

	glutSwapBuffers()

def mainReshape(w,h):
	if h == 0:
		h = 1
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity() 
	gluPerspective(45, float(w) / h, 0.1, 100)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def idle():
	glutPostRedisplay()

def drag(x,y):
	global prevX
	global prevY
	global eye
	global up
	diffX = x - prevX
	diffY = -y + prevY
	prevX = x
	prevY = y
	if abs(diffX) > 40 or abs(diffY) > 40:
		return
	eye = transform.left(diffX,eye,up)
	eye, up = transform.up(diffY,eye,up)

	glutPostRedisplay()

def keyboard(key,x,y):
	global knot
	if key == 27:
		exit(0)
	elif key == "+":
		knot.setSigma(knot.SIGMA*2.0)
	elif key == "-":
		knot.setSigma(knot.SIGMA/2.0)
	elif key == "o":
		knot.optimize()
	glutPostRedisplay()


def step(data):
	global knot
	glutTimerFunc(200,step,-1)
	glutPostRedisplay()

def mouse(button,state,x,y):
	global prevX
	global prevY
	if state == 1:
		prevX = 0
		prevY = 0

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE)
	glutInitWindowSize(640, 480)
	glutInitWindowPosition(0, 0)
	glutCreateWindow("Knot")
	glutDisplayFunc(mainDisplay)
	glutReshapeFunc(mainReshape)
	glutMotionFunc(drag)
	glutMouseFunc(mouse)
	glutKeyboardFunc(keyboard)
	glutTimerFunc(500,step,-1)
	# glutIdleFunc(idle)
	init()
	glutMainLoop()
	return

if __name__ == '__main__': main()
