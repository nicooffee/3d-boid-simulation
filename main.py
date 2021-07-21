import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from FlockOctree import Flock
from Boid import Boid
import asyncio
from ctypes import *
from multiprocessing import Process,Pipe, process
import random as r
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
flocks = []
col_fu = []
for i in range(4):
    flocks.append(Flock(D_MIN_X_C,D_MAX_X_C,D_MIN_Y_C,D_MAX_Y_C,D_MIN_Z_C,D_MAX_Z_C))
    rr = r.random()
    rg = r.random()
    rb = r.random()
    col_fu.append(lambda percent: (percent*rr,percent*rg,percent*rb,))
LARGO_FLOCK = len(flocks[0])
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


def flocking_process(flock,conn):
    flag = True
    while flag:
        flock.flocking()
        for boid_data in flock.show():
            conn.send(boid_data)
            conn.recv()

async def show_boid(conn,cant,color_function):
    i = 0
    while i<cant: #revisar esto
        coor,boid_in_range = conn.recv()
        percent = (boid_in_range*2)/cant
        color = color_function(percent)
        glColor3f(*color)
        glVertex3f(*(coor))
        conn.send(True)
        i = i + 1

# estoy usando len(flock) asumiendo que todos tienen el mismo largo
async def run_show_boid():
    tasks = []
    L = len(flocks)
    for i in range(L):
        tasks.append(show_boid(pipes[i][0],LARGO_FLOCK,col_fu[i]))
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
    #set_wall_grid()
    glEnd()
    glBegin(GL_POINTS)
    asyncio.run(run_show_boid())
    glEnd()
    glBegin(GL_LINES)
    set_upper_grid()
    glEnd()
    glPopMatrix()
    glFlush()    




pipes = []
processes = []

for i in range(len(flocks)):
    p_conn, c_conn = Pipe()
    pipes.append((p_conn,c_conn,))
    p = Process(target=flocking_process,args=(flocks[i],c_conn,))
    p.start()
    processes.append(p)

def keyboard_options(key,x,y):
    d_key = key.decode('utf-8')
    if key == b'\x1B': #ESCAPE \x[HEXADECIMAL]
        for p in processes:
            p.terminate()
        glutLeaveMainLoop()
        glutDestroyWindow(glutGetWindow())

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
glutKeyboardFunc(keyboard_options)
glutDisplayFunc(display)
glutIdleFunc(display)
glutMainLoop()