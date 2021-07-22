import numpy as np
import functools as ft
def translate(tx,ty):
    return np.matrix(
        [[1,0,tx],
        [0,1,ty],
        [0,0,1]])

def rotate(angle):
    r = 2*np.pi*angle / 360
    ca = np.cos(r)
    sa = np.sin(r)
    return np.matrix(
        [[ca,-sa,0],
        [sa, ca,0],
        [0 , 0 ,1]])

def scale(sx,sy):
    return np.matrix(
        [[sx,0,0],
        [0,sy,0],
        [0,0, 1]])

#La refleccion se hace en el punto x,y siendo el centro el origen
def reflect(x,y):
    m1 = translate(-x,-y)
    m2 = rotate(180)
    m3 = translate(x,y)
    return compose([m1,m2,m3])

def shear(shx,shy):
    return np.matrix(
        [[1,shx,0],
        [shy, 1,0],
        [0 , 0 ,1]])

def compose(tr_list):
    tr_list.reverse()
    return ft.reduce(lambda M,N: M*N,tr_list)

def rodrigues_rotation(axis,angle):
    r = 2*np.pi*angle / 360
    I = np.identity(3)
    K = np.matrix([
        [0,-axis.item(2,0),axis.item(1,0)],
        [axis.item(2,0),0,axis.item(0,0)],
        [-axis.item(1,0),axis.item(0,0),0]
    ])
    R = I + np.sin(r)*K + (1-np.cos(r))*(K*K)
    return R

def rotate_arbitrary(axis,angle):
    u,v,w = axis
    r = 2*np.pi*angle / 360
    cos = np.cos(r)
    sin = np.sin(r)
    R = [
        [u*u+(1-u*u)*cos,u*v*(1-cos)-w*sin,u*w*(1-cos)+v*sin,0],
        [u*v*(1-cos)+w*sin,v*v+(1-v*v)*cos,v*w*(1-cos)-u*sin,0],
        [v*w*(1-cos)-v*sin,v*w*(1-cos)+u*sin,w*w+(1-w*w)*cos,0],
        [0,0,0,1]
    ]
    return R