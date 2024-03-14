import numpy as np

def propagation_coeffs(alphai, alpha, reflectivity_index):

    dns2 = 2 * reflectivity_index
    kz = -np.sin(alphai)
    kt = -np.sqrt(np.sin(alphai)**2 - dns2)
    Ri = (kz-kt)/(kz+kt)

    kz = np.sin(alpha)
    kt = np.sqrt(np.sin(alpha)**2 - dns2)
    Rf = (kz-kt)/(kz+kt)
    return [1, Ri, Rf, Ri*Rf]


if __name__ == '__main__':
    alphai = np.deg2rad(0.2)
    alpha = np.linspace(0, 0.0145, 600)

    reflectivity_index = complex(4.88e-06, 7.37e-08)
    fc = propagation_coeffs(alphai, alpha, reflectivity_index)

    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(nrows = 2)
    axs[0].plot(alpha, np.abs(fc[2])**2)
    axs[1].plot(alpha, np.abs(fc[3])**2)
    plt.savefig('falala.jpg')
