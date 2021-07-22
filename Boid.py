import numpy as np
import random as r
import Vector as v
import time


"""#################################################################

VELM_MIN = Velocidad mínima del boid.
VELM_MAX = Velocidad máxima del boid.
ACLM_MIN = Aceleración mínima del boid.
ACLM_MAX = Aceleración máxima del boid.
CONC_MIN = Conciencia mínima del boid
CONC_MAX = Conciencia máxima del boid.

#################################################################"""

VELM_MIN = 10.0
VELM_MAX = 20.0
ACLM_MIN = 2.5
ACLM_MAX = 3.5
CONC_MIN = 10
CONC_MAX = 20

"""#################################################################
Clase Boid

Clase que representa a un boid en la simulación. Los parámetros de
velocidad, aceleración y conciencia son calculados aleatoriamente
según las variables globales del módulo.

La posición del boid es calculada aleatoriamente dentro de los
límites entregados en el constructor.

id              = id del boid.
radio           = Rango de visión.
angulo_vision   = Ángulo de visión en [0,180] grados.
[xyz]_limits    = Límites de posición.
posicion        = Posición en el espacio
velocidad       = Vector de velocidad
velocidad_max   = Magnitud máxima del vector de velocidad
fuerza_max      = Magnitudad máxima del vector de aceleración
conciencia      = Cantidad de boids a considerar en el movimiento

#################################################################"""
class Boid:
    def __init__(self,id,radio,min_x,max_x,min_y,max_y,min_z,max_z):
        self.id = id
        self.radio = radio
        self.angulo_vision = 135
        self.x_limits = [min_x,max_x]
        self.y_limits = [min_y,max_y]
        self.z_limits = [min_z,max_z]
        r_x = (max_x - min_x) * r.random() + min_x
        r_y = (max_y - min_y) * r.random() + min_y
        r_z = (max_z - min_z) * r.random() + min_z
        self.posicion = np.array([r_x,r_y,r_z])
        self.velocidad = np.array([r.random(),r.random(),r.random()])
        self.aceleracion = np.array([0.0,0.0,0,0])
        self.velocidad_max = (VELM_MAX-VELM_MIN) * r.random() + VELM_MIN
        self.fuerza_max = (ACLM_MAX-ACLM_MIN) * r.random() + ACLM_MIN
        self.conciencia = r.randint(CONC_MIN,CONC_MAX)
        self.last_boid_in_range = 0

    """mover:

        Método para actualizar la posición del boid. El método
        es llamado después de realizar el flocking. Antes de actualizar la posición,
        se comprueba si la posición x,y,z del boid está dentro del [0,5]% o [95,100]%
        de cada [xyz]_limits. Si se cumple, se suman vectores de aceleración contrarios
        a los límites establecidos. La aceleración total se suma al vector de velocidad
        y el vector de velocidad es sumado a la posición.

    """
    def mover(self):
        self.velocidad = v.limit(self.velocidad,self.velocidad_max)
        self.posicion = self.posicion + self.velocidad
        self.velocidad = self.velocidad + self.aceleracion
        self.aceleracion = np.zeros(3)
        npos = self.posicion - np.array([self.x_limits[0],self.y_limits[0],self.z_limits[0]])
        nlim_x = [0,self.x_limits[1]-self.x_limits[0]]
        nlim_y = [0,self.y_limits[1]-self.y_limits[0]]
        nlim_z = [0,self.z_limits[1]-self.z_limits[0]]
        percent_x = np.divide((npos[0] + nlim_x[0]),nlim_x[0]+nlim_x[1])
        percent_y = np.divide((npos[1] + nlim_y[0]),nlim_y[0]+nlim_y[1])
        percent_z = np.divide((npos[2] + nlim_z[0]),nlim_z[0]+nlim_z[1])
        #percent_x = np.divide((self.posicion[0] + self.x_limits[0]),self.x_limits[0]+self.x_limits[1])
        #percent_y = np.divide((self.posicion[1] + self.y_limits[0]),self.y_limits[0]+self.y_limits[1])
        #percent_z = np.divide((self.posicion[2] + self.z_limits[0]),self.z_limits[0]+self.z_limits[1])
        acl_rebote_x = np.zeros(3)
        acl_rebote_y = np.zeros(3)
        acl_rebote_z = np.zeros(3)
        inner_p = 0
        if percent_x < 0.05:
            inner_p = (percent_x-0.05)/(-0.05)
            acl_rebote_x = v.set_mag(np.array([1,0,0]),4*self.fuerza_max*inner_p)
        elif percent_x > 0.95:
            inner_p = (percent_x-0.95)/(1-0.95)
            acl_rebote_x = v.set_mag(np.array([-1,0,0]),4*self.fuerza_max*inner_p)
        if percent_y < 0.05:
            inner_p = (percent_y-0.05)/(-0.05)
            acl_rebote_y = v.set_mag(np.array([0,1,0]),4*self.fuerza_max*inner_p)
        elif percent_y > 0.95:
            inner_p = (percent_y-0.95)/(1-0.95)
            acl_rebote_y = v.set_mag(np.array([0,-1,0]),4*self.fuerza_max*inner_p)
        if percent_z < 0.05:
            inner_p = (percent_z-0.05)/(-0.05)
            acl_rebote_z = v.set_mag(np.array([0,0,1]),4*self.fuerza_max*inner_p)
        elif percent_z > 0.95:
            inner_p = (percent_z-0.95)/(1-0.95)
            acl_rebote_z = v.set_mag(np.array([0,0,-1]),4*self.fuerza_max*inner_p)
        self.velocidad = self.velocidad + acl_rebote_x + acl_rebote_y + acl_rebote_z

    """flock
    
        Método que calcula los 3 vectores de aceleración del boid según
        una lista de flocks a considerar (alineamiento, cohesion y separacion).
        
        Se iteran los boids con el límite de conciencia y se comprueba si es
        que el boid está en el rango de visión del boid. Si se cumple, se agrega
        la influencia del boid a los 3 vectores de aceleración. 

        Cuando se recorren todos los boids, se actualizan los vectores de aceleración
        según los límites establecidos y finalmente la aceleración final del boid se
        reemplaza por la suma de los 3 vectores.
    """
    def flock(self,flock):
        suma_a = np.zeros(3) #vector alineamiento
        suma_c = np.zeros(3) #vector cohesion
        suma_r = np.zeros(3) #vector separacion
        boid_added = 0
        boid_in_range = 0
        for boid in flock[:self.conciencia]:
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
        self.last_boid_in_range = len(flock)#cambiado de boid_in_range
        suma_a = v.limit(suma_a,self.fuerza_max)
        suma_r = v.limit(suma_r,self.fuerza_max)
        suma_c = v.limit(suma_c,self.fuerza_max)
        return suma_a+suma_r*1.17+suma_c


    def show(self):
        return self.posicion

    def coords(self):
        p = self.posicion
        return (p[0],p[1],p[2])

    def distancia(self,boid):
        return np.linalg.norm(self.posicion-boid.posicion)


    """ en_rango

        Método para calcular el ángulo entre dos vectores. Se utiliza 
        el vector de velocidad de self (hacia donde mira) y la posición del
        boid a comparar. Se retorna True si boid está dentro del rango de visión.
    """
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