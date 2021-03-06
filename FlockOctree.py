import sys
sys.path.append('./octrees')
from octrees import Octree
from Boid import Boid

"""#################################################################
Clase FlockInfo

Clase utilizada para enviar la información de un Flock.
#################################################################"""
class FlockInfo:
    def __init__(self,last_max_flock,cant_flocks):
        self._last_max_flock = last_max_flock
        self._cant_flocks = cant_flocks
    
    @property
    def last_max_flocks(self):
        return self._last_max_flock

    @property
    def cant_flocks(self):
        return self._cant_flocks



"""#################################################################
Clase Flock

Clase utilizada para mantener un Flock en movimiento.
Atributos:
    boids           = Lista de boids
    octree          = Octree de boids
    last_max_flock  = Máximo flock en el último instante

#################################################################"""
class Flock:
    # Constructor
    def __init__(self,min_x,max_x,min_y,max_y,min_z,max_z,radio=150,cant=30):
        self.boids = list()
        self.octree = Octree(((min_x-10, max_x+10), (min_y-10, max_y+10), (min_z-10, max_z+10)))
        self.last_max_flock = 0
        for i in range(cant):
            b = Boid(i,radio,min_x,max_x,min_y,max_y,min_z,max_z)
            self.boids.append(b)
            self.octree.insert(b.coords(),b)
    # Iterador
    def __iter__(self):
        for boid in self.boids:
            yield boid
    # Cantidad de flocks para len(object)
    def __len__(self):
        return len(self.boids)

    # get_info:
    # Retorna objeto FlockInfo con la información del flock.
    def get_info(self):
        return FlockInfo(self.last_max_flock,len(self.boids))

    # show:
    # Iterador de coordenadas de un boid para mostrar en pantalla.
    def show(self):
        for boid in self.boids:
            yield (boid.show(),boid.last_boid_in_range,boid.velocidad)

    # flocking:
    # Método para realizar el movimiento de todos los boids.
    # Por cada boid, se utiliza un Octree para encontrar todos los boids cercanos
    # a un boid respecto a una distancia.
    # El boid es eliminado del octree durante las operaciones y agregado al 
    # finalizar.
    def flocking(self):
        self.last_max_flock = 0 #maximo flock de esta tanda
        for boid in self.boids:
            p = boid.coords()
            try:
                self.octree.remove(p)
                dis_cor_val = self.octree.by_distance_from_point(p,boid.radio)
                boids_list = []
                for (i,b) in enumerate(map(lambda dcv_tuple: dcv_tuple[2],dis_cor_val)): #limitar con conciencia
                    boids_list.append(b)
                    if i>=boid.conciencia:
                        break
                boid.aceleracion = boid.flock(boids_list)
                boid.mover()
                if boid.last_boid_in_range > self.last_max_flock:
                    self.last_max_flock = boid.last_boid_in_range
                self.octree.insert(boid.coords(),boid)
            except Exception as e:
                print("error", e.__class__,e)





#tests
if __name__ == '__main__':
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
    print(list(flock.octree),len(list(flock.octree)))
    c = 50
    while c == 50:
        for b in flock.flocking():
            pass
        c = len(list(flock.octree))
        print(list(flock.octree),c)