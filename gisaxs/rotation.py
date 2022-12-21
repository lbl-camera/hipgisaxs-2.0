#! /usr/bin/env python

from math import sin,cos
import math as m
from common import xp
import numpy as np
import collections

def Rx(a):
    c = xp.cos(a)
    s = xp.sin(a)
    if isinstance(a, float):
        rotx = xp.zeros((1, 3, 3), dtype='f')
    else:
        rotx = xp.zeros((len(a), 3, 3), dtype='f')
    rotx[:,0,0] = 1
    rotx[:,1,1] = rotx[:,2,2] = c
    rotx[:,1,2] = -s
    rotx[:,2,1] = s
    return rotx

def Ry(a):
    c = xp.cos(a)
    s = xp.sin(a)
    if isinstance(a, float):
        roty = xp.zeros((1, 3, 3), dtype='f')
    else:
        roty = xp.zeros((len(a), 3, 3), dtype='f')
    roty[:,0,0] = roty[:,2,2] = c
    roty[:,1,1] = 1
    roty[:,0,2] = s
    roty[:,2,0] = -s
    return roty
  
def Rz(a):
    c = xp.cos(a)
    s = xp.sin(a)
    if isinstance(a, float):
        rotz = xp.zeros((1, 3, 3), dtype='f')
    else:
        rotz = xp.zeros((len(a), 3, 3), dtype='f')
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

    # build rotation matrix 
    if isinstance(orientations, collections.OrderedDict):
        axis, angles = orientations.popitem(last=False)
        rot = rotation_matrix(axis, angles)
        for axis, angles in orientations.items():
            rot = xp.matmul(rotation_matrix(axis, angles), rot) 
    else:
        raise ValueError('unknown datatype for orientations')

    # arrange q-values in 3xN matrix
    q = xp.vstack([qx.flatten(),qy.flatten(),qz.flatten()])

    # rotation
    qrot = xp.dot(rot, q)
    return qrot[:,0,:].squeeze(), qrot[:,1,:].squeeze(), qrot[:,2,:].squeeze()
