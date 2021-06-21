from Boid import Boid
import asyncio
class Flock:
    def __init__(self,min_x,max_x,min_y,max_y,min_z,max_z,radio=100,cant=20):
        self.boids = list()
        for i in range(cant):
            b = Boid(i,radio,min_x,max_x,min_y,max_y,min_z,max_z)
            self.boids.append(b)

    def __iter__(self):
        for boid in self.boids:
            yield boid

    def __len__(self):
        return len(self.boids)


    async def flocking(self):
        async def _async_flock(boid_list,boid):
            boid.aceleracion = await boid.flock(boid_list)
        tasks = []
        for boid in self.boids:
            tasks.append(_async_flock(self,boid))
        await asyncio.ensure_future(asyncio.gather(*tasks))
        for boid in self.boids:
            boid.mover()
            yield (boid.show(),boid.last_boid_in_range)

    def flocking2(self):
        for boid in self.boids:
            boid.aceleracion = boid.flock(self)
        for boid in self.boids:
            boid.mover()
            yield (boid.show(),boid.last_boid_in_range)