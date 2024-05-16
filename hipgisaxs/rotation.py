
try:
    import cupy as np
    from cupy import sin, cos
except ImportError:
    import numpy as np
    from numpy import sin, cos

def Rx(a):
    c = np.cos(a)
    s = np.sin(a)
    if isinstance(a, float):
        rotx = np.zeros((1, 3, 3), dtype='f')
    else:
        rotx = np.zeros((len(a), 3, 3), dtype='f')
    rotx[:,0,0] = 1
    rotx[:,1,1] = rotx[:,2,2] = c
    rotx[:,1,2] = -s
    rotx[:,2,1] = s
    return rotx

def Ry(a):
    c = np.cos(a)
    s = np.sin(a)
    if isinstance(a, float):
        roty = np.zeros((1, 3, 3), dtype='f')
    else:
        roty = np.zeros((len(a), 3, 3), dtype='f')
    roty[:,0,0] = roty[:,2,2] = c
    roty[:,1,1] = 1
    roty[:,0,2] = s
    roty[:,2,0] = -s
    return roty
  
def Rz(a):
    c = np.cos(a)
    s = np.sin(a)
    if isinstance(a, float):
        rotz = np.zeros((1, 3, 3), dtype='f')
    else:
        rotz = np.zeros((len(a), 3, 3), dtype='f')
    rotz[:,0,0] = rotz[:,1,1] = c
    rotz[:,1,0] = s
    rotz[:,0,1] = -s
    rotz[:,2,2] = 1
    return rotz

def rotation_matrix(axis, angles):
    if axis == 'x':
        return Rx(angles)
    if axis == 'y':
        return Ry(angles)
    if axis == 'z':
        return Rz(angles)
    return None

def rotate(qx, qy, qz, orientations):
    """
    Rotate q-values by given Euler angles.

    Parameters
    ----------
        qx : array_like
            q-values along x-axis.
        qy : array_like
            q-values along y-axis.
        qz : array_like
            q-values along z-axis.
        orientations : dict
            Dictionary containing axis and angles for rotation.
            Example: {'x': 0.1, 'y': 0.2, 'z': 0.3}

    Returns
    -------
        qx_rot : array_like
            Rotated q-values along x-axis.
        qy_rot : array_like
            Rotated q-values along y-axis.
        qz_rot : array_like
            Rotated q-values along z-axis.
    """

    # build rotation matrix 
    if isinstance(orientations, dict):
        rot = np.eye(3)
        for axis, angles in orientations.items():
            rot = np.matmul(rotation_matrix(axis, angles), rot) 
    else:
        raise ValueError('datatype for orientations must be dict')

    # arrange q-values in 3xN matrix
    q = np.vstack([qx.flatten(),qy.flatten(),qz.flatten()])

    # rotation
    qrot = np.dot(rot, q)
    return qrot[:,0,:].squeeze(), qrot[:,1,:].squeeze(), qrot[:,2,:].squeeze()
