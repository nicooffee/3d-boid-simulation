import numpy as np
import re
import goperation as go
import Vector as v
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
for i in range(5):
    flocks.append(Flock(D_MIN_X_C,D_MAX_X_C,D_MIN_Y_C,D_MAX_Y_C,D_MIN_Z_C,D_MAX_Z_C))
    rr = r.random()
    rg = r.random()
    rb = r.random()
    col_fu.append(lambda percent: (1-percent*rr,1-percent*rg,1-percent*rb,))
LARGO_FLOCK = len(flocks[0])
last_max_flock = [0] * LARGO_FLOCK
#----------------------------------------------------------------------------------------------#

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

def draw_coords():
    a = np.array([cpos_x,cpos_y,cpos_z])
    b = np.array([0,1,0]) # y
    v_axis = v.set_mag(np.cross(a,b),100)
    glBegin(GL_POINTS)
    glColor3f(1,1,1)
    glVertex3f(lkat_x,lkat_y,lkat_z)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(100,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,100,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,100)
    glColor3f(0,1,1)
    glVertex3f(0,0,0)
    glVertex3f(v_axis[0],v_axis[1],v_axis[2])
    glEnd()

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
        i = i + 1
    conn.send(True)

# estoy usando len(flock) asumiendo que todos tienen el mismo largo
async def run_show_boid():
    tasks = []
    L = len(flocks)
    for i in range(L):
        tasks.append(show_boid(pipes[i][0],LARGO_FLOCK,col_fu[i]))
    await asyncio.gather(*tasks)

pa = 0.1
cpos_x = MAX_X_C-200
cpos_y = MAX_Y_C-200
cpos_z = MIN_Z_C-200
lkat_x = 0
lkat_y = 0
lkat_z = 0

def setOrthographicProjection():
	# switch to projection mode
	glMatrixMode(GL_PROJECTION)
	# save previous matrix which contains the
	#settings for the perspective projection
	glPushMatrix()
	# reset matrix
	glLoadIdentity()
	# set a 2D orthographic projection
	gluOrtho2D(MIN_X_C, MAX_X_C, MAX_Y_C, MIN_Y_C)
	#switch back to modelview mode
	glMatrixMode(GL_MODELVIEW)
def restorePerspectiveProjection():
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def display():
    global pa,cpos_x,cpos_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.9,0.9,0.9,1)
    glPointSize(5.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0,0,MAX_Z_C*(1.8))
    gluLookAt(cpos_x,cpos_y,cpos_z,lkat_x,lkat_y,lkat_z,0,1,0)
    pa = pa + 0.01
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
    draw_coords()
    setOrthographicProjection()
    glPushMatrix()
    glLoadIdentity()
    print_menu(MIN_X_C+30,MIN_Y_C+30)
    glPopMatrix()
    restorePerspectiveProjection()
    glFlush()    

def print_menu(x,y):
    font = GLUT_BITMAP_9_BY_15
    def col(n): # [0...]
        return x+n*9
    def row(n): # [0...]
        return y+n*30
    glColor3f(0,0,0)
    glRasterPos2f(col(0),row(0))
    for c in f'PCAM: x:{cpos_x:.3f} y:{cpos_y:.3f} z:{cpos_z:.3f}':
        glutBitmapCharacter(font ,ord(c))
    glRasterPos2f(col(0),row(1))
    for c in f'Flocks: {len(flocks):}':
        glutBitmapCharacter(font ,ord(c))
    for i,f in enumerate(flocks):
        glRasterPos2f(col(0),row(2+i))
        for c in f'F{i:}: {f.last_max_flock}':
            glutBitmapCharacter(font ,ord(c))

pipes = []
processes = []

for i in range(len(flocks)):
    p_conn, c_conn = Pipe()
    pipes.append((p_conn,c_conn,))
    p = Process(target=flocking_process,args=(flocks[i],c_conn,))
    p.daemon = True
    p.start()
    processes.append(p)

def keyboard_options(key,x,y):
    global cpos_x,cpos_y,cpos_z
    d_key = key.decode('utf-8')
    if key == b'\x1B': #ESCAPE \x[HEXADECIMAL]
        for p in processes:
            p.terminate()
        glutLeaveMainLoop()
        glutDestroyWindow(glutGetWindow())
    elif bool(re.match('[wW]',d_key)):
        a = np.array([cpos_x,cpos_y,cpos_z])
        b = np.array([0,1,0]) # y
        ang = v.angle(a,b)
        if 45<=ang: #limite arriba
            v_axis = v.set_mag(np.cross(a,b),1)
            pos = np.matrix([[cpos_x],[cpos_y],[cpos_z],[1]])
            R = go.rotate_arbitrary(v_axis,2)
            new_pos = R * pos
            cpos_x = new_pos.item(0,0)
            cpos_y = new_pos.item(1,0)
            cpos_z = new_pos.item(2,0)
        
    elif bool(re.match('[sS]',d_key)):
        a = np.array([cpos_x,cpos_y,cpos_z])
        b = np.array([0,1,0]) # y
        ang = v.angle(a,b)
        if v.angle(a,b)<=135: #limite abajo
            v_axis = v.set_mag(np.cross(a,b),1)
            pos = np.matrix([[cpos_x],[cpos_y],[cpos_z],[1]])
            R = go.rotate_arbitrary(v_axis,-2)
            new_pos = R * pos
            cpos_x = new_pos.item(0,0)
            cpos_y = new_pos.item(1,0)
            cpos_z = new_pos.item(2,0)

    elif bool(re.match('[aA]',d_key)):
        new_pos_xz = np.matrix([[cpos_x],[cpos_z],[1]])
        new_pos_xz = go.rotate(2) * new_pos_xz
        cpos_x = new_pos_xz.item(0,0)
        cpos_z = new_pos_xz.item(1,0)
    elif bool(re.match('[dD]',d_key)):
        new_pos_xz = np.matrix([[cpos_x],[cpos_z],[1]])
        new_pos_xz = go.rotate(-2) * new_pos_xz
        cpos_x = new_pos_xz.item(0,0)
        cpos_z = new_pos_xz.item(1,0)
        pass

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