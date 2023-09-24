import numpy as np

def basic_reflectivity(alpha, reflectivity_index):

    dns2 = 2 * reflectivity_index
    kz = np.sin(alpha)
    kt = np.sqrt(np.sin(alpha)**2 - dns2)
    R = (kz - kt)/(kz + kt)
    return  R

def propagation_coeffs(alphai, alpha, reflectivity_index):

    Ri = basic_reflectivity(alphai, reflectivity_index)
    Rf = basic_reflectivity(alpha.ravel(), reflectivity_index)
    return [np.single(1.), Ri, Rf, Rf*Ri ] 
