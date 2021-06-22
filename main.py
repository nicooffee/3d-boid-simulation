import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from FlockOctree import Flock
from Boid import Boid
import asyncio
from ctypes import *

GRID_COLOR = (0,0,0.45)
GRID_SPACE = 40

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
flock2 = Flock(D_MIN_X_C,D_MAX_X_C,D_MIN_Y_C,D_MAX_Y_C,D_MIN_Z_C,D_MAX_Z_C)
flock3 = Flock(D_MIN_X_C,D_MAX_X_C,D_MIN_Y_C,D_MAX_Y_C,D_MIN_Z_C,D_MAX_Z_C)
flocks = [flock,flock2,flock3]
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


async def do_flock(f):
    #print("Procesando: {:}".format(i))
    for (coor,boid_in_range) in f.show():
        percent = (boid_in_range*10)/len(f)
        glColor3f(1.0 - percent,percent,percent)
        glVertex3f(*(coor))
    await f.flocking()
    #print("Resultado: {:}".format(i))
    #print(f)
async def run_flock():
    tasks = []
    for f in flocks:
        tasks.append(do_flock(f))
    await asyncio.gather(*tasks)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0,0.0,0.17,1)
    glPointSize(5.0)
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
    asyncio.run(run_flock())
    glEnd()
    glBegin(GL_LINES)
    set_upper_grid()
    glEnd()
    glPopMatrix()
    glFlush()    


loop = asyncio.get_event_loop()
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