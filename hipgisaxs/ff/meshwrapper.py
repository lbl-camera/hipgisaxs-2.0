
try:
    import cupy
except ImportError:
    pass
import numpy as np
from .meshff import meshff

"""
This function calculates the form factor of an object with a given mesh.

Parameters
----------
    qx : ndarray (float64)
    qy : ndarray (float64)
    qz : ndarray (complex128)
    rotation : ndarray (float64)
    vertices : numpy.ndarray (float64)

Returns
-------
    ff : numpy.ndarray (complex128)
        The form factor of the object with the given mesh.

"""
def MeshFF(qx, qy, qz, rotation, vertices):


    # ensure types
    if isinstance(qx, cupy.ndarray):
        using_gpu = True
        

    if using_gpu:
        qx = np.float64(qx.get())
        qy = np.float64(qy.get())
        qz = np.complex128(qz.get())
        rotation = np.float64(rotation.get())

    # vertices should be a numpy array
    vertices = np.float64(vertices)

    # Call the CUDA extension
    ff = meshff(qx, qy, qz, rotation, vertices)

    if using_gpu:
        ff = cupy.array(ff)
    return ff
