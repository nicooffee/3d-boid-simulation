import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from FlockOctree import Flock
from Boid import Boid

GRID_COLOR = (0.4,0.4,0.4)
GRID_SPACE = 20

MAX_X_C = 800
MIN_X_C = -MAX_X_C
MAX_Y_C = 800
MIN_Y_C = -MAX_Y_C
MAX_Z_C = 800
MIN_Z_C = -MAX_Z_C
D_MAX_X_C = MAX_X_C / 2
D_MIN_X_C = MIN_X_C / 2
D_MAX_Y_C = MAX_Y_C / 2
D_MIN_Y_C = MIN_Y_C / 2
D_MIN_Z_C = MIN_Z_C / 2
D_MAX_Z_C = MAX_Z_C / 2

flock = Flock(D_MIN_X_C,D_MAX_X_C,D_MIN_Y_C,D_MAX_Y_C,D_MIN_Z_C,D_MAX_Z_C)

def set_wall_grid():
    glColor3f(*GRID_COLOR)
    for i in np.arange(D_MIN_Y_C,D_MAX_Y_C+1,GRID_SPACE):
        glVertex3f(D_MIN_X_C,i,D_MIN_Z_C)
        glVertex3f(D_MIN_X_C,i,D_MAX_Z_C)
    for i in np.arange(D_MIN_Z_C,D_MAX_Z_C+1,GRID_SPACE):
        glVertex3f(D_MIN_X_C,D_MIN_Y_C,i)
        glVertex3f(D_MIN_X_C,D_MAX_Y_C,i)
    for i in np.arange(D_MIN_Y_C,D_MAX_Y_C+1,GRID_SPACE):
        glVertex3f(D_MIN_X_C,i,D_MAX_Z_C)
        glVertex3f(D_MAX_X_C,i,D_MAX_Z_C)
    for i in np.arange(D_MIN_X_C,D_MAX_X_C+1,GRID_SPACE):
        glVertex3f(i,D_MIN_Y_C,D_MAX_Z_C)
        glVertex3f(i,D_MAX_Y_C,D_MAX_Z_C)

def set_bottom_grid():
    glColor3f(*GRID_COLOR)
    for i in np.arange(D_MIN_X_C,D_MAX_X_C+1,GRID_SPACE):
        glVertex3f(i,D_MIN_Y_C,D_MIN_Z_C)
        glVertex3f(i,D_MIN_Y_C,D_MAX_Z_C)
    for i in np.arange(D_MIN_Z_C,D_MAX_Z_C+1,GRID_SPACE):
        glVertex3f(D_MIN_X_C,D_MIN_Y_C,i)
        glVertex3f(D_MAX_X_C,D_MIN_Y_C,i)

def set_upper_grid():
    glColor3f(*GRID_COLOR)
    for i in np.arange(D_MIN_X_C,D_MAX_X_C+1,GRID_SPACE):
        glVertex3f(i,D_MAX_Y_C,D_MIN_Z_C)
        glVertex3f(i,D_MAX_Y_C,D_MAX_Z_C)
    for i in np.arange(D_MIN_Z_C,D_MAX_Z_C+1,GRID_SPACE):
        glVertex3f(D_MIN_X_C,D_MAX_Y_C,i)
        glVertex3f(D_MAX_X_C,D_MAX_Y_C,i)


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(MIN_X_C,MAX_X_C,MIN_Y_C,MAX_Y_C,MIN_Z_C,MAX_Z_C)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    global n
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.05,0.05,0.05,1)
    glPointSize(10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glRotatef(-20,1,0,0)
    glTranslatef(0,0,MAX_Z_C*2)
    gluLookAt(MAX_X_C,MAX_Y_C,MIN_Z_C,MIN_X_C,MIN_Y_C,MAX_Z_C,0,1,0)
    glBegin(GL_LINES)
    set_bottom_grid()
    set_wall_grid()
    glEnd()
    glBegin(GL_POINTS)
    for (coor,boid_in_range) in flock.flocking():
        percent = (boid_in_range*2)/len(flock)
        glColor3f(1.0 - percent,percent,percent)
        glVertex3f(*(coor))
    glEnd()
    glBegin(GL_LINES)
    set_upper_grid()
    glEnd()
    glPopMatrix()
    glFlush()    


glutInit()
glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
glutInitWindowSize(900, 900)
glMatrixMode(GL_PROJECTION)
glOrtho(MIN_X_C,MAX_X_C,MIN_Y_C,MAX_Y_C,MIN_Z_C,MAX_Z_C)
glutCreateWindow("Flocking simulation")
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_FLAT)
glDisable(GL_CULL_FACE)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutIdleFunc(display)
glutMainLoop()