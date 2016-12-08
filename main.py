
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
azims = [0,0,0,-45.0,0]
azims = [40, 0, 0, 0.0, 0, 0, 120, 0, 120, 120, 15, 100, 120, 120, 30, 45]
# azims = [40, 0, 0, 0.0, 0, 0, 20, 0, 20, 20, 15, 10, 20, 20, 30, 45]
trans = [8,4,-5]
rot = [30,-50,10]
# azims = [44.80429237442888, -4.2376028891688025, 8.078777353992281, -47.629185542039586, 23.98956606948402, -62.40799126988669, 117.03008939731846, 24.189136552534286, 223.9971350171729, 53.52623220783585, -1.6917141393291961, 46.59393778327448, 305.3573161374373, 2.339866839971895, 29.318816351384665, 176.26504667056665]
# azims = [42.66869579052874, -0.31974522814420064, -3.556266470078884, 3.497303205401314, -34.95965415842811, 6.740473396965431, -17.621914081908656, 29.87370799428534, -99.02234507673073, 126.1019368057637, -56.27025991549906, -0.3701145794456697, 53.956827372345955, 0.4067178466013154, -1.0800684283205975, 39.785773052614175]
utx = -55
uty = 0
utz = 0
ux = -3.34
uy = 0
uz = 0

optimizing = False
knot = bd.Knot(azims)

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
	global ux
	global utx
	global knot
	global trans
	global rot
	# knot.buildEnds(trans,rot)
	knot.buildKnot()
	# knot.buildTrefoil(azims,utx,ux)
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
	if (type(knot.end1a) is list):
		l = [knot.end1a,knot.end1b,knot.end2a,knot.end2b]
		for i in range(len(l)):
			for p in range(len(l[i])):
				# print l[i][p]
				if i == 1 and p == 0:
					glVertex3fv(l[i][p])
				elif i == 3 and p == 2:
					glVertex3fv(l[i][p])
	else:
		#we have numpy arrays
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
	global utx
	global ux
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
		# knot.optimizeSingle()
	elif key == "+":
		# if knot.optimizing:
			#adjust step size bigger
		knot.setSigma(knot.sigma*2)
	elif key == "-":
		# if knot.optimizing:
			#adjust step size smaller
		knot.setSigma(knot.sigma/2)
	elif key == "x":
		if knot.optimizing:
			knot.stopOptimizing()
	elif key == "a":
		#change utx
		utx += 1
		print "utx now ",utx
	elif key == "A":
		#change utx
		utx -= 1
		print "utx now ",utx
	elif key == "z":
		#change ux
		ux += 0.01
		print "ux now ",ux
	elif key == "Z":
		#change ux
		ux -= 0.01
		print "ux now ",ux

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
