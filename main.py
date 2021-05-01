import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Flock import Flock
from Boid import Boid

MIN_X_C = 0
MAX_X_C = 640
MIN_Y_C = 0
MAX_Y_C = 480

flock = Flock(MIN_X_C,MAX_X_C,MIN_Y_C,MAX_Y_C)

# Return a random float in the range 0.0 to 1.0.
def randomFloat():
    return random.uniform(0,1)

# On reshape, uses an orthographic projection with world coordinates ranging
# from 0 to 1 in the x and y directions, and -1 to 1 in z.
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(MIN_X_C,MAX_X_C,MIN_Y_C,MAX_Y_C)


# Clears the window then plots 20 fish bitmaps in random colors at random
# positions.
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.15,0.15,0.15,1)
    glPointSize(10.0)
    glBegin(GL_POINTS)
    for boid in flock:
        boid.flock(flock)
        boid.mover()
        percent = (boid.last_c_neigh+10)/len(flock)
        glColor3f(1.0 - percent,percent,percent)
        glVertex2f(*(boid.show()))
    glEnd()
    glFlush()    


glutInit()
glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
glutInitWindowSize(640, 480)
gluOrtho2D(MIN_X_C,MAX_X_C,MIN_Y_C,MAX_Y_C)
glutCreateWindow("Flocking simulation")
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutIdleFunc(display)
glutMainLoop()