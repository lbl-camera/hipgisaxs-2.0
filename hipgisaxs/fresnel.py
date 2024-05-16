# Description: This file contains the function that calculates 
# the reflection and transmission coefficients of a dielectric interface.

try:
    import cupy as np
except ImportError:
    import numpy as np 

def propagation_coeffs(alphai, alpha, reflectivity_index):
    """ Calculate the reflection and transmission coefficients of a dielectric interface.
    Parameters:
        alphai: angle of incidence
        alpha: angle of refraction
        reflectivity_index: refractive index of the dielectric interface

    Returns:
        [1, Ri, Rf, RiRf]: Reflection and transmission coefficients
    """

    dns2 = 2 * reflectivity_index
    kz = np.sin(alphai)
    kt = np.sqrt(np.sin(alphai)**2 - dns2)
    Ri = (kz-kt)/(kz+kt)

    kz = np.sin(alpha)
    kt = np.sqrt(np.sin(alpha)**2 - dns2)
    Rf = (kz-kt)/(kz+kt)
    return [1, Ri, Rf, Ri*Rf]


