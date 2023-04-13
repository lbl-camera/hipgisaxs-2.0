
import os
import json
import config

def load_experiment(config):
    if os.path.exist("experiment.json"):
        expf = "experiment.json"
   
        with open(expf, 'r') as fp:
            ex = json.load(fp)

        if 'sdd' in ex:
            config.sdd = ex['sdd']

        if 'energy' in ex:
            config.wavelength = 1.23984e+03 / ex['energy']

        if 'beam_center' in ex:
            config.beam_center = ex[beam_center]

        

    
     

