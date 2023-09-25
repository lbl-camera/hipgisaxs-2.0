import json
from tqdm import tqdm
import subprocess

# data 

energy = [ 250, 283, 285, 287 ]

refidx =[
    ((1.969e-03, 1.439e-04),  (1.954e-03, 1.439e-04)),
    ((-4.977e-04, 3.956e-05),  (-6.084e-04, 3.587e-05)),
    ((-1.374E-03, 3.365e-03), (-1.414e-03, 3.700e-03)),
    ((-1.898e-03, 1.709e-03), (-2.031e-03, 1.743e-03))
    ]

experiments = {}
for k, v in zip(energy, refidx):
    experiments[k] = v

# instrumentation
infA = 'json/instrument1.json'
outfA = 'json/instrument.json'
with open(infA) as fp:
    instrument = json.load(fp)

# sample
infB = 'json/sample1.json'
outfB = 'json/sample.json'
with open(infB) as fp:
    sample = json.load(fp)

for e, n in tqdm(experiments.items()):
    n1, n2 = n
    sample['unitcell'][0]['delta'] = n1[0] 
    sample['unitcell'][0]['beta'] = n1[1] 
    sample['unitcell'][1]['delta'] = n2[0] 
    sample['unitcell'][1]['beta'] = n2[1] 

    instrument['energy'] = e

    # write input files
    for ai in tqdm(range(5,20)):
        instrument['incident_angle'] = ai

        with open(outfA, 'w') as fp:
            json.dump(instrument, fp, indent = 4) 

        with open(outfB, 'w') as fp:
            json.dump(sample, fp, indent = 4) 

        subprocess.run(['python', 'main.py'])
