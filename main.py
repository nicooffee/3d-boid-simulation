"""#################################################################
# Proyecto gráfico - Simulación flock
#
# Nombre:  Nicolás Honorato
# Fecha:   20/08/2021 
# Descripción:
#   Aplicación gráfica que simula el comportamiento de flocking de 
#   las aves o peces. Se utiliza un proceso por flock y cada flock
#   es independiente.
#   
#   El tamano inicial de la pantalla esta definido por las variables
#   MIN_X_C, MAX_X_C | MIN_Y_C, MAX_Y_C. La profundidad está
#   definida por las variables MIN_Z_C, MAX_Z_C
#   
#   GRID_COLOR  = Color del grid.
#   BG_COLOR    = Color del background.
#   GRID_SPACE  = Espacio entre lineas del grid.
#   CANT_FLOCKS = Cantidad de flocks a simular.
#   LARGO_FLOCK = Cantidad de boid en un flock.
#################################################################"""
import numpy as np
import re
import goperation as go
import Vector as v
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from FlockOctree import Flock,FlockInfo
from Boid import Boid
import asyncio
from ctypes import *
from multiprocessing import Process,Pipe,Queue
import random as r
GRID_COLOR  = (0,0,0.45)
BG_COLOR    = (0.9,0.9,0.9,1)
GRID_SPACE = 40
CANT_FLOCKS = 5
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
for i in range(CANT_FLOCKS):
    flocks.append(Flock(D_MIN_X_C,D_MAX_X_C,D_MIN_Y_C,D_MAX_Y_C,D_MIN_Z_C,D_MAX_Z_C))
    rr = r.random()
    rg = r.random()
    rb = r.random()
    col_fu.append(lambda percent: (1-percent*rr,1-percent*rg,1-percent*rb,))
LARGO_FLOCK = len(flocks[0])
flocks_info = [FlockInfo(0,LARGO_FLOCK)] * CANT_FLOCKS

cpos_x = MAX_X_C-200        # Posición x cámara
cpos_y = MAX_Y_C-200        # Posición y cámara
cpos_z = MIN_Z_C-200        # Posición z cámara
lkat_x = 0                  # Posición x punto a mirar por la cámara
lkat_y = 0                  # Posición y punto a mirar por la cámara
lkat_z = 0                  # Posición z punto a mirar por la cámara
#----------------------------------------------------------------------------------------------#

"""set_wall_grid
    Función que muestra el grid vertical en 3 caras.
"""
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

"""set_bottom_grid
    Función que muestra el grid inferior.
"""
def set_bottom_grid():
    glColor3f(*GRID_COLOR)
    for i in np.arange(D_MIN_X_C,D_MAX_X_C+1,GRID_SPACE):
        glVertex3f(i,D_MIN_Y_C,D_MIN_Z_C)
        glVertex3f(i,D_MIN_Y_C,D_MAX_Z_C)
    for i in np.arange(D_MIN_Z_C,D_MAX_Z_C+1,GRID_SPACE):
        glVertex3f(D_MIN_X_C,D_MIN_Y_C,i)
        glVertex3f(D_MAX_X_C,D_MIN_Y_C,i)


"""set_upper_grid
    Función que muestra el grid superior.
"""
def set_upper_grid():
    glColor3f(*GRID_COLOR)
    for i in np.arange(D_MIN_X_C,D_MAX_X_C+1,GRID_SPACE):
        glVertex3f(i,D_MAX_Y_C,D_MIN_Z_C)
        glVertex3f(i,D_MAX_Y_C,D_MAX_Z_C)
    for i in np.arange(D_MIN_Z_C,D_MAX_Z_C+1,GRID_SPACE):
        glVertex3f(D_MIN_X_C,D_MAX_Y_C,i)
        glVertex3f(D_MAX_X_C,D_MAX_Y_C,i)

"""draw_coords
    Función que muestra los ejes desde la coordenada (0,0,0) en
    coordenadas positivas. 
    Rojo -> x
    Verde -> y
    Azul -> z
    Cyan -> Producto cruz entre y el vector de la pos actual.
"""
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

"""reshape
    Función para el comportamiento de la aplicación cuando
    se cambia el tamaño de la pantalla
"""
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(MIN_X_C,MAX_X_C,MIN_Y_C,MAX_Y_C,MIN_Z_C,MAX_Z_C)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


"""flocking_process
    Función ejecutada en proceso independiente que realiza el
    flocking de un flock particular. Envía mensajes recibidos en
    proceso principal para mostrar el boid. Cuando termina una
    instancia de flocking, envía a flock_info_queue la información 
    del flock.
"""
def flocking_process(id,flock,conn,flock_info_queue):
    flag = True
    while flag:
        flock.flocking()
        for boid_data in flock.show():
            conn.send(boid_data)
        conn.recv()
        try:
            flock_info_queue.put_nowait((id,flock.get_info()))
        except Exception:
            pass

"""show_boid
    Función asíncrona para mostrar un boid en pantalla. Recibe
    un mensaje desde flocking_process con la posición del flock.
    Cuando termina el ciclo, le envía un mensaje al proceso que
    le indica que ya finalizó.
"""
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

"""run_show_boid
    Función que ejecuta la función show_boid para cada proceso de 
    forma asíncrona. 
"""
# estoy usando len(flock) asumiendo que todos tienen el mismo largo
async def run_show_boid():
    tasks = []
    L = len(flocks)
    for i in range(L):
        tasks.append(show_boid(pipes[i][0],LARGO_FLOCK,col_fu[i]))
    await asyncio.gather(*tasks)

"""
    Función que consume los elementos de flock_info_queue enviados
    por un flocking_process.
"""
def consume_queue():
    for i in range(10):
        try:
            (i,flock_info) = flock_info_queue.get_nowait()
            flocks_info[i] = flock_info
        except Exception:
            break


# Cambia la proyección a 2d para escribir el menu
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

# Recupera la proyección luego de escribir el menu
def restorePerspectiveProjection():
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

"""display
    Función principal que muestra el contenido de la simulación.
"""
def display():
    global cpos_x,cpos_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*BG_COLOR)
    glPointSize(5.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0,0,MAX_Z_C*(1.8))
    gluLookAt(cpos_x,cpos_y,cpos_z,lkat_x,lkat_y,lkat_z,0,1,0)
    glBegin(GL_LINES)
    set_bottom_grid()                       # Grid inferior
    #set_wall_grid()
    glEnd()
    glBegin(GL_POINTS)
    asyncio.run(run_show_boid())            # Mostrar los boid async
    glEnd()
    glBegin(GL_LINES)
    set_upper_grid()                        # Grid superior
    glEnd()
    if d_coors:
        draw_coords()                       # Mostrar ejes en el 0,0 y el producto cruz
    consume_queue()                         # Consumir cola de info flock
    setOrthographicProjection()
    glPushMatrix()
    glLoadIdentity()
    print_menu(MIN_X_C+30,MIN_Y_C+30)       # Mostrar menu (aunque no es un menu)
    glPopMatrix()
    restorePerspectiveProjection()
    glFlush()    

"""print_menu
    Función que muestra el texto en pantalla.
"""
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
    for c in f'Flocks: {CANT_FLOCKS:}':
        glutBitmapCharacter(font ,ord(c))
    glRasterPos2f(col(0),row(2))
    for c in f'Maximo flock actual:':
        glutBitmapCharacter(font ,ord(c))
    for i in range(CANT_FLOCKS):
        glRasterPos2f(col(0),row(3+i))
        for c in f'F{i+1}: {flocks_info[i].last_max_flocks:3} /{flocks_info[i].cant_flocks:3}':
            glutBitmapCharacter(font ,ord(c))


pipes = []                          # Conexiones entre proceso principal y flocks
processes = []                      # Procesos
flock_info_queue = Queue(10)        # Cola de info flock
d_coors = True                      # Mostrar coordenadas

# Creación de procesos por cada flock
for i in range(len(flocks)):
    p_conn, c_conn = Pipe()
    pipes.append((p_conn,c_conn,))
    p = Process(target=flocking_process,args=(i,flocks[i],c_conn,flock_info_queue,))
    p.daemon = True
    p.start()
    processes.append(p)

def keyboard_options(key,x,y):
    global cpos_x,cpos_y,cpos_z,d_coors
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
    elif bool(re.match('[bB]',d_key)):
        d_coors = False if d_coors else True


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