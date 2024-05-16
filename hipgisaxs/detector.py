
# This file contains the Detector class which is used to define the detector

try:
    import cupy as np
    from cupy import cos, sin
except ImportError:
    import numpy as np
    from numpy import cos, sin

class Detector:
    """
    Detector class to define the detector geometry. 
    The detector is defined by the name, shape, and pixel size.
    It is used to calculate the q-vectors and q-values for the detector.
    """
    
    def __init__(self, name, shape, pixle_size):
        self.name = name
        self.shape = shape
        self.pixle_size = pixle_size

    @classmethod
    """
    Create a detector object from the JSON object.
    """
    
    def from_dict(cls, det):
        n = det['name'] 
        rows = det['pixel_rows']
        cols = det['pixel_cols']
        pixel = det['pixel_size']
        return cls(n, [rows, cols], pixel)        

    """
    Calculate the angles from the center of the sample to the detector.
    
    Parameters:
        sdd: sample to detector distance
        center: center of beam on the detector
    """
    def angles(self, sdd, center):
        nrow = self.shape[0]
        ncol = self.shape[1]
        y, x = np.mgrid[0:nrow, 0:ncol]

        # shift coordinate with center
        x = (x - center[0]) * self.pixle_size[0]
        y = (y - center[1]) * self.pixle_size[1]

        # angles 
        tmp = np.sqrt(x**2 + sdd**2)
        theta = np.arcsin(x/tmp)
        alpha = np.arctan2(y, tmp)
        return theta, alpha

    """
    Calculate the q-vectors for the detector.

    Parameters:
        sdd: sample to detector distance
        center: center of beam on the detector
        energy: energy of the x-ray

    Returns:
        qx, qy, qz: q-vectors for the detector
    """
    def qvectors(self, sdd, center, energy):

        wavelen = 1.23094e+03 / energy
        theta, alpha = self.angles(sdd, center)
        theta = theta.ravel()
        alpha = alpha.ravel()

        # radius of Ewald's sphere
        k0 = 2 * np.pi / wavelen

        # q-vector
        qx = k0 * (cos(alpha) * cos(theta) - 1)
        qy = k0 * (cos(alpha) * sin(theta))
        qz = k0 * (sin(alpha))
        return qx, qy, qz

    """
    Calculate the q-values for the detector.

    Parameters:
        sdd: sample to detector distance
        center: center of beam on the detector
        energy: energy of the x-ray

    Returns:
        q: q-values for the detector
    """
    def qvalues(self, sdd, center, energy):

        wavelen = 1230.94 / energy
        q = self.qvectors(sdd, center, wavelen)
        return np.linalg.norm(q, axis=1)



    """
    Calculate the q-vectors, including the four qz-components, for the experimental geometry.

    Parameters:
        sdd: sample to detector distance
        center: center of beam on the detector
        energy: energy of the x-ray
        alphai: incident angle

    Returns:
        qx, qy, [qz1...qz4]: q-vectors for the detector
    """
    def dwba_qvectors(self, sdd, center, energy, alphai):

        theta, alpha = self.angles(sdd, center)
        theta = theta.ravel()
        alpha = alpha.ravel()

        wavelen = 1230.94 / energy

        # radius of the Ewald's sphere
        k0 = 2 * np.pi / wavelen

        # q-vector
        qx = k0 * (cos(alpha) * cos(theta) - cos(alphai))
        qy = k0 * (cos(alpha) * sin(theta))
        kzf = k0 * sin(alpha)
        kzi = -k0 * sin(alphai)

        # (Ti, Tf)
        q1 = kzf - kzi

        # (Ri, Tf)
        q2 = kzf + kzi

        # (Ti, Rf)
        q3 = -kzf - kzi

        # (Ri, Rf)
        q4 = -kzf + kzi

        return qx, qy, [q1, q2, q3, q4]
        
