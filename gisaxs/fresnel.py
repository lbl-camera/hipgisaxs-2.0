#! /usr/bin/env python
from common import xp

def basic_reflectivity(alpha, reflectivity_index):

    dns2 = 2 * reflectivity_index
    kz = xp.sin(alpha)
    kt = xp.sqrt(xp.sin(alpha)**2 - dns2)
    R = (kz - kt)/(kz + kt)
    return  R

def propagation_coeffs(alphai, alpha, reflectivity_index):

    Ri = basic_reflectivity(alphai, reflectivity_index)
    Rf = basic_reflectivity(alpha, reflectivity_index)
    return [xp.single(1.), Ri, Rf, Rf*Ri ] 
