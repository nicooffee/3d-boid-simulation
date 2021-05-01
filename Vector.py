import numpy as np

def limit(V,fuerza_max):
    l = np.linalg.norm(V)
    if l>=fuerza_max:
        return V * (fuerza_max/l)
    return V

def set_mag(V,mag: float):
    if np.linalg.norm(V)>0:
        return np.divide(V,np.linalg.norm(V)) * mag
    return V