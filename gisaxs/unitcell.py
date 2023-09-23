import numpy as np
from .ff import cylinder, cone, cuboid

# cone.py  cuboid.py  cylinder.py  sphere.py

_baseVars = ['delta', 'beta', 'locations', 'orient']

def makeShapeObject(shape):
    fftype = shape['formfactor']
    if fftype == 'Cone':
        ob = Cone()
        Vars = _baseVars + ['radius', 'height', 'angle']
    elif fftype == 'Cyliner':
        ob = Cyliner()
        Vars = _baseVars + ['radius', 'height']
    elif fftype == 'Cuboid':
        ob = Cuboid()
        Vars = _baseVars + ['length', 'width', 'height']
    elif fftype == 'Sphere':
        ob = Sphere()
        Vars = ['radius'] 
    else:
        raise ValueError('Unknown formfactor')

    # set rest of the attributes
    for name in Vars:
        if name in shape:
            setattr(ob, name, shape[name])
        else:
            setattr(ob, name, None)
    return ob



class Unitcell:
    def __init__(self, shapes, delta = 0, beta = 0):

        self.shapes = []
        self.n1 = 1 - complex(delta, beta)
        for shape in shapes:
            self.shapes.append(makeShapeObject(shape)) 

    def calcff(self, qx, qy, qz):
        ff = np.zeros(qx.shape, dtype=complex)
        for shape in self.shapes:
            n2 = 1 - complex(shape.delta, shape.beta)
            tempff = shape.ff(qx, qy, qz)
            locs = shape.locations
            dnsq = self.n1**2 - n2**2
            for l in locs:
                tempff = tempff * np.exp(1j*(qx*l[0]+qy*l[1]+qz*l[2])) 
            ff += tempff;
        return (dnsq * ff)


# ----basic shapes------#
class Cyliner:
    def __init__(self):
        pass 

    # calculate form-factor
    def ff(self, qx, qy, qz):
        return cylinder(qx, qy, qz, self.radius, self.height, self.orient)

class Cuboid:
    def __init__(self):
        pass 

    # calculate form-factor
    def ff(self, qx, qy, qz):
        return cuboid(qx, qy, qz, self.length, self.width, self.height, self.orient)

class Cone:
    def __init__(self):
        pass

    # calculate form-factor
    def ff(self, qx, qy, qz):
        return cone(qx, qy, qz, self.radius, self.height, self.angle, self.orient)

class Sphere:
    def __init__(self):
        pass

    # calculate form-factor
    def ff(self, qx, qy, qz):
        return sphere(qx, qy, qz, self.radius)
