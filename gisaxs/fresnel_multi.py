
import numpy as np

class Layer:
    def __init__(self, delta, beta, order, thickness):
        self.one_n2 = 2 * complex(delta, beta)
        self.order = order
        self.thickness = thickness
        self.zval = 0

class MultiLayer:
    def __init__(self):
        self.layers = [Layer(0, 0, 0, 0)]
        self.substrate = Layer(4.88E-6, 7.37E-08, -1, 0)
        self._setup_ = False

    def insert(self, layer):
        if not isinstance(layer, Layer):
            raise TypeError('only Layer types can be inserted into multilayered object')
            exit(101)
        if not layer.order > 0:
            raise ValueError('the order of layer must be greater than 0');
            exit(102)
        self.layers.insert(layer.order, layer)
    
    def setup_multilayer(self):
        if self._setup_ : return

        # put substrate at the end
        self.layers.append(self.substrate)

        # calc z of every interface
        nlayer = len(self.layers)
        self.layers[0].zval = 0
        for i in range(1, nlayer-1):
            self.layers[i].zval = self.layers[i-1].zval + self.layers[i].thickness
        self.layers[-1].zval = np.inf

        # run only once
        self._setup_ = True

    def parratt_recursion(self, alpha, k0, order):
        self.setup_multilayer()
        nlayer = len(self.layers)
        shape = np.shape(alpha)
        # account for scalar case
        if len(shape) == 0:
            shape = (1,)

        # sin(alpha)
        sin_a = np.sin(alpha)

        # initialize
        dims = (nlayer-1,) + shape
        dim2 = (nlayer, ) + shape

        # cacl k-value
        kz = np.zeros(dim2, np.complex_)
        for i in range(nlayer):
            kz[i,:] =  k0 * np.sqrt(sin_a**2 - self.layers[i].one_n2)

        # calculate Rs
        R = np.zeros(dim2, dtype=np.complex_)
        T = np.zeros(dim2, dtype=np.complex_)
        T[-1] = 1
        for i in reversed(range(nlayer-1)):
            z = self.layers[i].zval
            en = np.exp(-1j * kz[i] * z)
            ep = np.exp( 1j * kz[i] * z)
            t0 = (kz[i] + kz[i+1]) / (2 * kz[i])
            t1 = (kz[i] - kz[i+1]) / (2 * kz[i])
            T[i] = T[i+1] * en * t0 + R[i+1] * en * t1
            R[i] = T[i+1] * ep * t1 + R[i+1] * ep * t0

        T0 = T[0]
           
        return T[order]/T0, R[order]/T0

    def propagation_coeffs(self, alphai, alpha, k0, order):
        Ti, Ri = self.parratt_recursion(alphai, k0, order)
        Tf, Rf = self.parratt_recursion(alpha, k0, order)
        fc = np.zeros((4,) + alpha.shape, np.complex_)
        
        fc[0,:] = Ti * Tf
        fc[1,:] = Ri * Tf
        fc[2,:] = Ti * Rf
        fc[3,:] = Ri * Rf
        fc[:,alpha < 0] = 0
        return fc
