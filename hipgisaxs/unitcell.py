from abc import ABC

try:
    import cupy as np
except ImportError:
    import numpy as np

import warnings

from .ff import cuboid, cone, cone_stack, cone_shell, cylinder, sphere

try:
    from .ff import MeshFF
except ImportError:
    warnings.warn('failed to import meshff, required for triangulated structures', stacklevel=2)

def makeShapeObject(shape):
    fftype = shape.pop('formfactor')
    if fftype in globals():
        ob = globals()[fftype](**shape)
    else:
        raise ValueError('Unknown formfactor')
    return ob


class ShapeBase(ABC):
    def __init__(self, delta, beta, locations=None, orient=None):
        self.delta = delta
        self.beta = beta
        self.locations = locations
        self.orient = orient

    def ff(self, qx, qy, qz):
        pass


class CoreShell(ShapeBase):
    def __init__(self, core, shell):
        self.core = makeShapeObject(core)
        self.shell = makeShapeObject(shell)

        super().__init__(delta=shell.delta,
                         beta=shell.beta,
                         locations=shell.locations,
                         orient=shell.orient)

    def ff(self, qx, qy, qz):
        ff_core = self.core.ff(qx, qy, qz)
        refidx_core = 2 * complex(self.core.delta, self.core.beta)
        ff_shell = self.shell.ff(qx, qy, qz) - ff_core
        refidx_shell = 2 * complex(self.shell.delta, self.shell.beta)
        return (ff_shell + (refidx_core - refidx_shell) * ff_core)


class Unitcell:
    def __init__(self, shapes, delta=0, beta=0):

        self.shapes = []
        self.ns2 = 2 * complex(delta, beta)
        for shape in shapes:
            if shape['formfactor'] == 'CoreShell':
                self.shapes.append(CoreShell(shape))
            else:
                self.shapes.append(makeShapeObject(shape))

    def ff(self, qx, qy, qz):
        ff = np.zeros(qx.size, dtype=complex)
        for shape in self.shapes:
            dn2 = 2 * complex(shape.delta, shape.beta) - self.ns2
            tempff = shape.ff(qx, qy, qz)
            locs = shape.locations
            if locs is None:
                locs = [{'x': 0, 'y': 0, 'z': 0}]
            for l in locs:
                tempff += tempff * np.exp(1j * (qx * l['x'] + qy * l['y'] + qz * l['z']))
            ff += tempff;
        return ff


# ----basic shapes------#
class Cyliner(ShapeBase):
    def __init__(self, *args, radius, height, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius
        self.height = height 

    # calculate form-factor
    def ff(self, qx, qy, qz):
        return cylinder(qx, qy, qz, self.radius, self.height, self.orient)


class Cuboid(ShapeBase):
    def __init__(self, *args, length, width, height, **kwargs):
        super().__init__(*args, **kwargs)
        self.length = length
        self.width = width
        self.height = height

    # calculate form-factor
    def ff(self, qx, qy, qz):
        return cuboid(qx, qy, qz, self.length, self.width, self.height, self.orient)


class Cone(ShapeBase):
    def __init__(self, *args, radius, height, angle, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius
        self.height = height
        self.angle = angle

    # calculate form-factor
    def ff(self, qx, qy, qz):
        return cone(qx, qy, qz, self.radius, self.height, self.angle, self.orient)


class Sphere(ShapeBase):
    def __init__(self, *args, radius, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    # calculate form-factor
    def ff(self, qx, qy, qz):
        return sphere(qx, qy, qz, self.radius)


"""
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
"""
