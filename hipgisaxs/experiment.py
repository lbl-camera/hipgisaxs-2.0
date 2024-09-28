
class Experiment:
    def __init__(self, instrument, sample):
        self.instrument = instrument
        self.sample = sample
        self.output = output

    def run(self, **kwargs):

        # get q-vectors
        qx, qy, qz = self.instrument.detector.dwba_qvectors()

        # get fresnel coefficients
        _, alpha = self.instrument.detector.angles()
        alphai = self.instrument.incident_angle
        fc = sample.substrate.propegation_coeffs(alphai, alpha)

        # calculate DWBA
        data = np.zeros_like(qx, dtype=complex)
        for i in range(4):
            ff = self.sample.unitcell.ff(qx, qy, qz[i])
            sf = structure_factor(qx, qy, qz[i], dspace, numelms, orient)
            data += fc[i] * sf * ff 
        return data


def setup_experiment(instrument, sample, output):
    instrument_obj = build_instrument(instrument)
    sample_obj = build_sample(sample)
    output_obj = build_output(output)
    experiment = Experiment(instrument_obj, sample_obj, output_obj)
    return experiment
    
