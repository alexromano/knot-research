
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import transform
import numpy as np
import builder as bd
eye = np.array([0.0,-13.0,1.5])
up = np.array([0.0,0.0,1.0])

prevX = 0
prevY = 0
r = 0

edges = [
[0,1],
[1,2],
[2,3],
[3,4],
[4,5],
[5,6],
[6,7],
[7,8],
[8,9],
[9,10],
[10,11],
[11,12],
[12,13],
[13,14],
[14,15],
[15,0]
]
# azims = [0,0,0,-45.0,0,0,15,15]
azims = [20,20,20,20,20,20,20,20,100,100,100,100,100,100,100,100]
# azims = [20.130276310621998, 16.558409431835692, 15.151145015055574, -21.149336793460066, 82.85660752538558, -126.22683154632516, 80.00352835773987, -48.01690161445404, 59.054255033897476, 29.37069404749205, 264.478342772936, 59.50846683110751, 36.91104683858014, 156.04815229055808, 104.59333784123578, 41.68161439480237]
utx = 55
uty = 0
utz = 0
ux = 03
uy = 0
uz = 0

optimizing = False
knot = bd.Knot()

def init():
	# glLightModeli(GL_LIGHT_MODEL_TWO_SIDE,GL_TRUE)
	# glEnable(GL_DEPTH_TEST)
	# glEnable(GL_LIGHTING)
	# glEnable(GL_LIGHT0)

	# glLightfv(GL_LIGHT0, GL_AMBIENT, [0.8,0.8,0.8,10,0])
	# glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0,1.0,1.0,10,0])
	# glLightfv(GL_LIGHT0, GL_POSITION, [1,1,1,0.0])

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
	glVertex3f(10.0,0.0,0.0)
	# y axis
	glColor3f(0.0,1.0,0.0)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(0.0,10.0,0.0)
	# z axis
	glColor3f(0.0,0.0,1.0)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(0.0,0.0,10.0)

	glEnd()
	#built knot and draw modules
	global azims
	global knot
	knot.buildKnot(azims)
	knot.currCost = knot.cost()[2]
	for module in knot.modules:

		glBegin(GL_LINES)
		glColor3f(1.0, 0.0, 0.0);
		mod = module[0]
		b = mod[:mod.shape[0]/2]
		m = mod[mod.shape[0]/2:]
		for edge in edges:
			for v in edge:
				glVertex3fv(b[v])
		for edge in edges:
			for v in edge:
				glVertex3fv(m[v])
		for i in range(mod.shape[0]/2):
			glVertex3fv(b[i])
			glVertex3fv(m[i])
		glEnd()

		glBegin(GL_LINES)
		glColor3f(0.0,1.0,0.0)
		mod = module[1]
		b = mod[:mod.shape[0]/2]
		m = mod[mod.shape[0]/2:]
		for edge in edges:
			for v in edge:
				glVertex3fv(b[v])
		for edge in edges:
			for v in edge:
				glVertex3fv(m[v])
		for i in range(mod.shape[0]/2):
			glVertex3fv(b[i])
			glVertex3fv(m[i])
		glEnd()

	#draw end points
	glBegin(GL_POINTS)
	glColor(1.0,1.0,1.0)
	glVertex3fv(knot.end1a)
	glVertex3fv(knot.end1b)
	glVertex3fv(knot.end2a)
	glVertex3fv(knot.end2b)
	glEnd()

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
	eye = transform.left(diffX,eye,up)
	eye, up = transform.up(diffY,eye,up)

	prevX = x
	prevY = y
	glutPostRedisplay()

def keyboard(key,x,y):
	global knot
	global azims
	incMap = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'q':10,'w':11,'e':12,'r':13,'t':14,'y':15}
	decMap = {')':0,'!':1,'@':2,'#':3,'$':4, '%':5, '^':6, '&':7,'*':8, '(':9,
	'Q':10, 'W':11, 'E':12, 'R':13, 'T':14, 'Y':15}

	if key == 27:
		exit(0)
	elif key in incMap.keys():
		i = incMap[key]
		if i < len(azims):
			azims[i] += 10
			knot.printStats()
	elif key in decMap.keys():
		i = decMap[key]
		if i < len(azims):
			azims[i] -= 10
			knot.printStats()
	elif key == "o":
		# if not knot.optimizing:
		# 	#save current azims and start optimizing
		# 	# initialAzims = 
		# 	knot.startOptimizing()
		knot.optimize()
	elif key == "+":
		# if knot.optimizing:
			#adjust step size bigger
		knot.setSigma(knot.sigma*4)
	elif key == "-":
		# if knot.optimizing:
			#adjust step size smaller
		knot.setSigma(knot.sigma/4)
	elif key == "x":
		if knot.optimizing:
			knot.stopOptimizing()

	glutPostRedisplay()


def step(data):
	global knot
	# if knot.optimizing:
		# global r
		# r += 1
		# if r == 10:
		# 	print "dislaying"
		# 	glutPostRedisplay()
		# 	r = 0
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
	glutCreateWindow("Circle")
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
