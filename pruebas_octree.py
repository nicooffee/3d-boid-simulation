import sys
sys.path.append('./octrees')
from octrees import Octree
from Boid import Boid

o = Octree(((0.0, 1.0), (0.0, 1.0), (0.0, 1.0)))
o.insert((0.33, 0.66, 0.99), Boid(1,20,0,1,0,1,0,1))
o.insert((0.12, 0.34, 0.56), Boid(2,20,0,1,0,1,0,1))
o.insert((0.98, 0.76, 0.54), Boid(3,20,0,1,0,1,0,1))
for p in o:
    print(p)
o2 = o.deform(lambda p: (p[0]+0.1,p[1],p[2]))
for p in o2:
    print(p)