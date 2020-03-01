import numpy as np
from math import *

def to_unit_vector(vec):
    np_vec = np.array(vec)

    # TODO make sure these singularity checks actually work
    if np_vec.any():
        return np.true_divide(np_vec, np.sqrt((np_vec ** 2).sum()))

    return np_vec

def llarToWorld(lat, lon, alt, rad):
    # see: http://www.mathworks.de/help/toolbox/aeroblks/llatoecefposition.html
    f  = 0                              # flattening
    ls = atan((1 - f)**2 * tan(lat))    # lambda

    x = rad * cos(ls) * cos(lon) + alt * cos(lat) * cos(lon)
    y = rad * cos(ls) * sin(lon) + alt * cos(lat) * sin(lon)
    z = rad * sin(ls) + alt * sin(lat)

    return np.array([x, y, z])


"""
# Test Code
if __name__ == "__main__":
    vec = [-1508, 16452, -264]
    print("Vector: " + str(vec))
    print("Unit: " + str(to_unit_vector(vec)))

    llar = llarToWorld(18.93, 62.0, 80, 1)
    print (llar)
"""