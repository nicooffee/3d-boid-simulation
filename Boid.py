import numpy as np
import random as r
import Vector as v
import time
class Boid:
    def __init__(self,id,radio,min_x,max_x,min_y,max_y):
        self.id = id
        self.radio = radio
        self.x_limits = [min_x,max_x]
        self.y_limits = [min_y,max_y]
        r_x = (max_x - min_x) * r.random() + min_x
        r_y = (max_y - min_y) * r.random() + min_y
        self.posicion = np.array([r_x,r_y])
        self.velocidad = np.array([r.random(),r.random()])
        self.aceleracion = np.array([0.0,0.0])
        self.fuerza_max = 2
        self.velocidad_max = 10.0
        self.last_c_neigh = 0


    def mover(self):
        self.velocidad = v.limit(self.velocidad,self.velocidad_max)
        self.posicion = self.posicion + self.velocidad
        self.velocidad = self.velocidad + self.aceleracion
        if self.posicion[0] > self.x_limits[1]:
            self.posicion[0] = self.x_limits[0]
        elif self.posicion[0] < self.x_limits[0]:
            self.posicion[0] = self.x_limits[1]
        if self.posicion[1] > self.y_limits[1]:
            self.posicion[1] = self.y_limits[0]
        elif self.posicion[1] < self.y_limits[0]:
            self.posicion[1] = self.y_limits[1]


    def flock(self,flock):
        #fuerza_alineamiento = v.limit(self.alinear(flock),self.fuerza_max)
        #fuerza_cohesion = v.limit(self.cohesionar(flock),self.fuerza_max)
        #fuerza_separacion = v.limit(self.separar(flock),self.fuerza_max)
        self.aceleracion = self.update_acr(flock)#fuerza_alineamiento + fuerza_cohesion + fuerza_separacion

    def update_acr(self,flock):
        suma_a = np.zeros(2)
        suma_c = np.zeros(2)
        suma_r = np.zeros(2)
        boid_added = 0
        for boid in flock:
            if boid.id != self.id and self.en_rango(boid):
                suma_a = suma_a + boid.velocidad
                suma_c = suma_c + boid.posicion
                dif = self.posicion - boid.posicion
                suma_r = suma_r + np.divide(dif,self.distancia(boid))
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
        self.last_c_neigh = boid_added
        suma_a = v.limit(suma_a,self.fuerza_max)
        suma_r = v.limit(suma_r,self.fuerza_max)
        suma_c = v.limit(suma_c,self.fuerza_max)
        return suma_a+suma_c+suma_r

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

    def show(self):
        return self.posicion

    def distancia(self,boid):
        return np.linalg.norm(self.posicion-boid.posicion)

    def en_rango(self,boid):
        return self.distancia(boid)<=self.radio
    #########################################################