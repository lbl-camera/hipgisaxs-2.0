import numpy as np

def propagation_coeffs(alphai, alpha, reflectivity_index):

    dns2 = 2 * reflectivity_index
    kz = np.sin(alphai)
    kt = np.sqrt(np.sin(alphai)**2 - dns2)
    Ri = (kz-kt)/(kz+kt)

    kz = np.sin(alpha)
    kt = np.sqrt(np.sin(alpha)**2 - dns2)
    Rf = (kz-kt)/(kz+kt)
    return [1, Ri, Rf, Ri*Rf]


