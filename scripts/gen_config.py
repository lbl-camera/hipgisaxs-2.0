import numpy as np
import json


horizontal = (-10.32, 13.34, 5254)
vertical = (-5.16, 14.83, 4439)
incident = 3.4

alpha = np.linspace(np.deg2rad(vertical[0]),   np.deg2rad(vertical[1]),   vertical[2])
theta = np.linspace(np.deg2rad(horizontal[0]), np.deg2rad(horizontal[1]), horizontal[2])
theta, alpha  = np.meshgrid(theta, alpha)

# CeO2 = {0.000190109844  0.000224374395}
config = {
    'energy': 878, # nanometer
    'incident': incident,
    'theta': theta.tolist(),
    'alpha': alpha.tolist(),
    'delta': 5.333E-04,
    'beta':  8.2545E-05,
    'cone': {'radius': 60., 'height': 24.3, 'angle': 50.5 },
    'lattice': [[200,0,0],[0,200,0],[0,0,1]],
    'repeats': [500, 500, 0]
}
with open('../json/config.json', 'w') as fp: json.dump(config, fp)

