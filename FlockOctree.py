import sys
sys.path.append('./octrees')
from octrees import Octree
from Boid import Boid
class Flock:
    def __init__(self,min_x,max_x,min_y,max_y,min_z,max_z,radio=150,cant=40):
        self.boids = list()
        self.octree = Octree(((min_x-10, max_x+10), (min_y-10, max_y+10), (min_z-10, max_z+10)))
        self.last_max_flock = 0
        for i in range(cant):
            b = Boid(i,radio,min_x,max_x,min_y,max_y,min_z,max_z)
            self.boids.append(b)
            self.octree.insert(b.coords(),b)
    def __iter__(self):
        for boid in self.boids:
            yield boid

    def __len__(self):
        return len(self.boids)

    def show(self):
        for boid in self.boids:
            yield (boid.show(),boid.last_boid_in_range)

    def flocking(self):
        self.last_max_flock = 0 #maximo flock de esta tanda
        for boid in self.boids:
            p = boid.coords()
            try:
                self.octree.remove(p)
                dis_cor_val = self.octree.by_distance_from_point(p,boid.radio)
                boid.aceleracion = boid.flock(list(map(lambda dcv_tuple: dcv_tuple[2],dis_cor_val)))
                boid.mover()
                if boid.last_boid_in_range > self.last_max_flock:
                    self.last_max_flock = boid.last_boid_in_range
                self.octree.insert(boid.coords(),boid)
            except Exception as e:
                print("error", e.__class__,e)






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