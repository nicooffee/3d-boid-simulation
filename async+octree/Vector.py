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

def angle(V,U):
    V_unit = np.divide(V,np.linalg.norm(V))
    U_unit = np.divide(U,np.linalg.norm(U))
    cos_ang = np.dot(V_unit,U_unit)
    return np.rad2deg(np.arccos(cos_ang))