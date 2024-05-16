try:
    import cupy as np
except ImportError:
    import numpy as np

import warnings

from .ff import  cuboid, cone, cone_stack, cone_shell, cylinder, sphere, trapezoid, trapezoid_stack

try:
    from .ff import MeshFF
except ImportError:
    warnings.warn('failed to import meshff, required for triangulated structures', stacklevel=2)
    

# cone.py  cuboid.py  cylinder.py  sphere.py

_baseVars = ['delta', 'beta', 'locations', 'orient']

def makeShapeObject(shape):
    fftype = shape['formfactor']
    if fftype == 'Cone':
        ob = Cone()
        Vars = _baseVars + ['radius', 'height', 'angle']
    elif fftype == 'Cylinder':
        ob = Cyliner()
        Vars = _baseVars + ['radius', 'height']
    elif fftype == 'Cuboid':
        ob = Cuboid()
        Vars = _baseVars + ['length', 'width', 'height']
    elif fftype == 'Sphere':
        ob = Sphere()
        Vars = _baseVars + ['radius'] 
    elif fftype == 'ConeStack':
        ob = ConeStack()
        Vars = _baseVars + ['radius', 'height', 'angles']
    elif fftype == 'ConeShell':
        ob = ConeShell()
        Vars = _baseVars + ['outer_radius', 'inner_radius', 'height', 'outer_angle', 'inner_angle']
    elif fftype == 'meshff':
        ob = MeshFT()
        Vars = _baseVars + ["meshfile"]
    else:
        raise ValueError('Unknown formfactor')

    # set rest of the attributes
    for name in Vars:
        if name in shape:
            setattr(ob, name, shape[name])
        else:
            setattr(ob, name, None)
    return ob

class CoreShell:
    def __init__(self, shape):
        self.core = makeShapeObject(shape['Core'])
        self.shell = makeShapeObject(shape['Shell'])
        self.delta = self.shell.delta
        self.beta = self.shell.beta
        self.locations = self.shell.locations

    def ff(self, qx, qy, qz):
        ff_core = self.core.ff(qx, qy, qz)
        refidx_core = 2 * complex(self.core.delta, self.core.beta)
        ff_shell = self.shell.ff(qx, qy, qz) - ff_core
        refidx_shell = 2 * complex(self.shell.delta, self.shell.beta)
        return (ff_shell + (refidx_core-refidx_shell) * ff_core)
         
class Unitcell:
    def __init__(self, shapes, delta = 0, beta = 0):

        self.shapes = []
        self.ns2 = 2*complex(delta, beta)
        for shape in shapes:
            if shape['formfactor'] == 'CoreShell':
                self.shapes.append(CoreShell(shape))
            else:
                self.shapes.append(makeShapeObject(shape)) 

    def ff(self, qx, qy, qz):
        ff = np.zeros(qx.size, dtype=complex)
        for shape in self.shapes:
            dn2 = 2* complex(shape.delta, shape.beta) - self.ns2
            tempff = shape.ff(qx, qy, qz)
            locs = shape.locations
            if locs is None:
                locs = [{'x':0, 'y':0, 'z':0}]
            for l in locs:
                tempff += tempff * np.exp(1j*(qx*l['x']+qy*l['y']+qz*l['z'])) 
            ff += tempff;
        return ff


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

class ConeStack:
    def __init__(self):
        pass

    def ff(self, qx, qy, qz):
        return cone_stack(qx, qy, qz, self.radius, self.height, self.angles, self.orient)

class ConeShell:
    def __init__(self):
        pass

    def ff(self, qx, qy, qz):
        return cone_shell(qx, qy, qz, self.outer_radius, self.inner_radius, self.height, self.outer_angle, self.inner_angle, self.orient)

class MeshFT:
    def __init__(self):
        pass

    def ff(self, qx, qy, qz):
        from stl import mesh
        mesh = mesh.Mesh.from_file(self.meshfile) 
        vertices = mesh.vectors.astype(float)
        qz = qz.astype(complex)
        rot = np.eye(3)
        return MeshFF(qx, qy, qz, rot, vertices)

