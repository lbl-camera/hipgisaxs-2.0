import numpy as np 

class Substrate:
    def __init__(self, reflectivity_index):
        self.reflectivity_index = reflectivity_index

    def propagation_coeffs(self, alphai, alpha):
    """ Calculate the reflection and transmission coefficients of a dielectric interface.
    Parameters:
        alphai: angle of incidence
        alpha: angle of refraction

    Returns:
        [1, Ri, Rf, RiRf]: Reflection and transmission coefficients
    """

    dns2 = 2 * self.reflectivity_index
    kz = np.sin(alphai)
    kt = np.sqrt(np.sin(alphai)**2 - dns2)
    Ri = (kz-kt)/(kz+kt)

    kz = np.sin(alpha)
    kt = np.sqrt(np.sin(alpha)**2 - dns2)
    Rf = (kz-kt)/(kz+kt)
    return [1, Ri, Rf, Ri*Rf]


