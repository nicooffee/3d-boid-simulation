import numpy as np
import random as r
import Vector as v
import time

VELM_MIN = 10.0
VELM_MAX = 10.0
ACLM_MIN = 1
ACLM_MAX = 2.0

class Boid:
    def __init__(self,id,radio,min_x,max_x,min_y,max_y):
        self.id = id
        self.radio = radio
        self.angulo_vision = 135
        self.x_limits = [min_x,max_x]
        self.y_limits = [min_y,max_y]
        r_x = (max_x - min_x) * r.random() + min_x
        r_y = (max_y - min_y) * r.random() + min_y
        self.posicion = np.array([r_x,r_y])
        self.velocidad = np.array([r.random(),r.random()])
        self.aceleracion = np.array([0.0,0.0])
        self.velocidad_max = (VELM_MAX-VELM_MIN) * r.random() + VELM_MIN
        self.fuerza_max = (ACLM_MAX-ACLM_MIN) * r.random() + ACLM_MIN
        self.last_boid_in_range = 0


    def mover(self):
        self.velocidad = v.limit(self.velocidad,self.velocidad_max)
        self.posicion = self.posicion + self.velocidad
        self.velocidad = self.velocidad + self.aceleracion
        self.aceleracion = np.zeros(2)
        percent_x = np.divide((self.posicion[0] + self.x_limits[0]),self.x_limits[0]+self.x_limits[1])
        percent_y = np.divide((self.posicion[1] + self.y_limits[0]),self.y_limits[0]+self.y_limits[1])
        acl_rebote_x = np.zeros(2)
        acl_rebote_y = np.zeros(2)
        inner_p = 0
        if percent_x < 0.05:
            inner_p = (percent_x-0.05)/(-0.05)
            acl_rebote_x = v.set_mag(np.array([1,0]),4*self.fuerza_max*inner_p)
        elif percent_x > 0.95:
            inner_p = (percent_x-0.95)/(1-0.95)
            acl_rebote_x = v.set_mag(np.array([-1,0]),4*self.fuerza_max*inner_p)
        if percent_y < 0.05:
            inner_p = (percent_y-0.05)/(-0.05)
            acl_rebote_y = v.set_mag(np.array([0,10]),4*self.fuerza_max*inner_p)
        elif percent_y > 0.95:
            inner_p = (percent_y-0.95)/(1-0.95)
            acl_rebote_y = v.set_mag(np.array([0,-1]),4*self.fuerza_max*inner_p)
        self.velocidad = self.velocidad + acl_rebote_x + acl_rebote_y


    def flock(self,flock):
        suma_a = np.zeros(2) #vector alineamiento
        suma_c = np.zeros(2) #vector cohesion
        suma_r = np.zeros(2) #vector separacion
        boid_added = 0
        boid_in_range = 0
        for boid in flock:
            d = self.distancia(boid)
            if d<=self.radio:
                boid_in_range += 1
            if boid.id != self.id and self.en_rango(boid):
                suma_a = suma_a + boid.velocidad
                suma_c = suma_c + boid.posicion
                dif = self.posicion - boid.posicion
                suma_r = suma_r + np.divide(dif,d if d>0 else 0.00001)
                boid_added = boid_added + 1
        if boid_added > 0:
            suma_a = np.divide(suma_a,boid_added)
            suma_a = v.set_mag(suma_a,self.velocidad_max)
            suma_a = suma_a - self.velocidad
            suma_c = np.divide(suma_c,boid_added)
            suma_c = suma_c - self.posicion
            suma_c = v.set_mag(suma_c,self.velocidad_max)
            suma_c = suma_c - self.velocidad
            suma_r = np.divide(suma_r,boid_added)
            suma_r = v.set_mag(suma_r,self.velocidad_max)
            suma_r = suma_r - self.velocidad
        self.last_boid_in_range = boid_in_range
        suma_a = v.limit(suma_a,self.fuerza_max)
        suma_r = v.limit(suma_r,self.fuerza_max)
        suma_c = v.limit(suma_c,self.fuerza_max)
        return suma_a+suma_r*1.35+suma_c


    def show(self):
        return self.posicion

    def distancia(self,boid):
        return np.linalg.norm(self.posicion-boid.posicion)

    def en_rango(self,boid):
        return self.distancia(boid) <= self.radio and v.angle(self.velocidad,boid.posicion-self.posicion) <= self.angulo_vision

    #########################################################


'''
    def alinear(self,flock):
        suma = np.zeros(2)
        boid_added = 0
        for boid in flock:
            if boid.id != self.id and self.en_rango(boid):
                suma = suma + boid.velocidad
                boid_added = boid_added + 1
        if boid_added > 0:
            suma = np.divide(suma,boid_added)
            suma = v.set_mag(suma,self.velocidad_max)
            suma = suma - self.velocidad
        self.last_c_neigh = boid_added
        return suma

    def cohesionar(self,flock):
        suma = np.zeros(2)
        boid_added = 0
        for boid in flock:
            if boid.id != self.id and self.en_rango(boid):
                suma = suma + boid.posicion
                boid_added = boid_added + 1
        if boid_added > 0:
            suma = np.divide(suma,boid_added)
            suma = suma - self.posicion
            suma = v.set_mag(suma,self.velocidad_max)
            suma = suma - self.velocidad
        self.last_c_neigh = boid_added
        return suma

    def separar(self,flock):
        suma = np.zeros(2)
        boid_added = 0
        for boid in flock:
            if boid.id != self.id and self.en_rango(boid):
                dif = self.posicion - boid.posicion
                dif = np.divide(dif,self.distancia(boid))
                suma = suma + dif
                boid_added = boid_added + 1
        if boid_added > 0:
            suma = np.divide(suma,boid_added)
            suma = v.set_mag(suma,self.velocidad_max)
            suma = suma - self.velocidad
        self.last_c_neigh = boid_added
        return suma

'''