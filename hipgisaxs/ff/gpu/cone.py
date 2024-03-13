import cupy as xp


gpu_cone_ff = xp.RawKernel(r'''

#include <cupy/complex.cuh>

extern "C" __device__
complex<float> cone_form_factor(
    float qx, float qy, float qz, float radius, float height, float angle) {

    // constants
    const float PI = 3.14159265359;
    const complex<float> J = complex<float>(0, 1);
    int num_nodes = 9;
    float node[] = {-0.96816, -0.836031, -0.613371, -0.324253, 0, 0.324253, 0.613371, 0.836031, 0.96816};
    float wght[] = {0.0812744, 0.180648, 0.260611, 0.312347, 0.330239, 0.312347, 0.260611, 0.180648, 0.0812744};

    float tan_a = tan(angle);
    float r_h = radius - height / tan_a;
    float qp = sqrt(qx * qx + qy * qy);
    float qzp = qz * tan_a;

    complex<float> t1 = 2 * PI * tan_a * exp(J * qzp * radius);
    complex<float> accuml = 0;
    for (int i = 0; i < num_nodes; i++) {
        float r = (r_h + radius) / 2 + (r_h - radius) / 2 * node[i];
        accuml += wght[i] * (r * r * exp(-J * qzp * r) * j1(qp * r) / (qp * r));
    }
    complex<float> ff = ((r_h - radius) / 2) * accuml;
    return ff * t1;
}

extern "C" __global__
void ff_cone_kernel(int nq, 
                    const float * qx, 
                    const float * qy,
                    const float * qz,
                    int num_vars,
                    const float * radius,
                    const float * height,
                    const float * angles,
                    complex<float>* ff) {

    int tid = blockDim.x * blockIdx.x + threadIdx.x;

    if (tid < nq) {
        for (int i = 0; i < num_vars; i++)
            ff[tid] += cone_form_factor(qx[tid], qy[tid], qz[tid], 
                                    radius[i], height[i], angles[i]);
    }
}

''', 'ff_cone_kernel')


def gpuFFCone(qx, qy, qz, radius, height, angles):

    nq = qx.size
    num_params = xp.int32(radius.size)

    ff = xp.zeros(qx.shape, dtype=xp.complex64) 

    # cuda kernel call
    threads = 256
    blocks = qx.size // threads
    if qx.size % threads > 0:
        blocks += 1
    gpu_cone_ff((blocks,), (threads,), (nq, qx, qy, qz, num_params, radius, height, angles, ff))

    return ff


