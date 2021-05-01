from Boid import Boid
class Flock:
    def __init__(self,min_x,max_x,min_y,max_y,radio=120,cant=50):
        self.boids = list()
        for i in range(cant):
            b = Boid(i,radio,min_x,max_x,min_y,max_y)
            self.boids.append(b)

    def __iter__(self):
        for boid in self.boids:
            yield boid

    def __len__(self):
        return len(self.boids)


    def flocking(self):
        for boid in self.boids:
            boid.aceleracion = boid.flock(self)
        for boid in self.boids:
            boid.mover()
            yield (boid.show(),boid.last_c_neigh)