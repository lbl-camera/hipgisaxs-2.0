#include <stdio.h>
#include <iostream>


#include "types.h"
#include "cuda_utils.cuh"
#include "cmplx_utils.cuh"
#include "rotation.h"

namespace hig {


    __device__ cucomplex_t 
    ffTriangle (const triangle_t & tri, const cucomplex_t * q){

        // constants
        constexpr double TINY = 1.0E-20;
        const cucomplex_t j1 = make_cucomplex(0, 1);
        const cucomplex_t jn = make_cucomplex(0,-1);

        // initialize stuff
        cucomplex_t ff = 0;

        // calculate q^2
        double q_sq = norm3(q);

        // form vertices
        vector3_t vertex[3];
        vertex[0] = vector3_t(tri.v1.x_, tri.v1.y_, tri.v1.z_);
        vertex[1] = vector3_t(tri.v2.x_, tri.v2.y_, tri.v2.z_);
        vertex[2] = vector3_t(tri.v3.x_, tri.v3.y_, tri.v3.z_);

        // form edges
        vector3_t edge[3];
        edge[0] = vertex[1] - vertex[0];
        edge[1] = vertex[2] - vertex[1];
        edge[2] = vertex[0] - vertex[2];

        // calculate outward normal and normalize
        vector3_t n_t = cross(edge[0], edge[1]);
        double  t_area = 0.5 * n_t.abs();
        n_t /= 2 * t_area;
 
        // dot (q, n_t)
        cucomplex_t q_dot_nt = dot(q, n_t);

        // calculate projection
        double proj_tq = q_sq - cuda::std::norm(q_dot_nt);

        // CASE 1
        if (cuda::std::abs(proj_tq) < TINY){
            cucomplex_t q_dot_v = dot(q, vertex[0]);

            // calculate Form-Factor
            ff = j1 * q_dot_nt * t_area / q_sq * cuda::std::exp(jn * q_dot_v);
        } else {

            // iterate on each edge :
            for (int e = 0; e < 3; e++) {

                // edge normal
                vector3_t n_e = cross(edge[e], n_t);
                n_e /= n_e.abs(); // normalize

                // dot(q, n_e)
                cucomplex_t q_dot_ne = dot(q, n_e);

                // proj_ne
                double proj_eq = proj_tq - cuda::std::norm(q_dot_ne);

                // CASE 2
                if (cuda::std::abs(proj_eq) < TINY){

                    // q_dot_v
                    cucomplex_t q_dot_v = dot(q, vertex[e]);

                    // calculate contribution of edge
                    double f0 = edge[e].abs() / (q_sq * proj_tq);
                    cucomplex_t f1 = - q_dot_nt * q_dot_ne;
                    cucomplex_t f2 = cuda::std::exp(jn * q_dot_v);
                    auto tmp = (f0 * f1 * f2);
                    ff += tmp;
                } else {
                    // CASE 3 (General case)
                    int e1 = (e+1) % 3;
                    double f0 = q_sq * proj_tq * proj_eq;
                    cucomplex_t f1 = jn * q_dot_nt * q_dot_ne;
                    cucomplex_t f2 = dot(q, edge[e]) / edge[e].abs();
                    cucomplex_t t1 = dot(q, vertex[e]);
                    cucomplex_t f3 = cuda::std::exp(jn * t1);
                    cucomplex_t t2 = dot(q, vertex[e1]);
                    cucomplex_t f4 = cuda::std::exp(jn * t2);
                    auto tmp = f1 * f2 * (f3-f4) / f0;
                    ff += tmp;
                }
            }
        }
        return ff;
    }

    __global__ void ff_tri_kernel1 (
            unsigned int nq, 
            const double *qx, const double *qy, const cucomplex_t *qz,
            int num_triangles, const triangle_t * triangles,
            const RotMatrix_t rot, cucomplex_t * ff) {

        unsigned int i = blockDim.x * blockIdx.x + threadIdx.x;
        if ( i < nq ) {
            cucomplex_t mq[3];
            rot.rotate(qx[i], qy[i], qz[i], mq);
            ff[i] = 0;
            for (int j=0; j < num_triangles; j++)
                ff[i] += ffTriangle(triangles[j], mq);
        } 
    } 

  /**
   * The main host function called from outside, as part of the API for a single node.
   */
  void FFTriangulation(
            int num_triangles, const triangle_t * triangles,
            int nq, const double * qx, const double * qy, 
            const cucomplex_t * qz, const RotMatrix_t rot,
            cucomplex_t *ff) { 
      
        double *d_qx, *d_qy;
        cucomplex_t *d_qz;
        cucomplex_t *d_ff;
        triangle_t *d_triangles;

        // allocate space for ff
        SAFE_CALL(cudaMalloc((void **) &d_ff, nq * sizeof(cucomplex_t)));

        // Allocate memory for qx, qy, qz
        SAFE_CALL(cudaMalloc((void **) &d_qx, nq * sizeof(cucomplex_t)));
        SAFE_CALL(cudaMalloc((void **) &d_qy, nq * sizeof(cucomplex_t)));
        SAFE_CALL(cudaMalloc((void **) &d_qz, nq * sizeof(cucomplex_t)));
        // Allocate memory for triangles
        SAFE_CALL(cudaMalloc((void **) &d_triangles, num_triangles * sizeof(triangle_t)));

        // copy buffers to device memory
        SAFE_CALL(cudaMemcpy(d_qx, qx, nq * sizeof(double), cudaMemcpyHostToDevice));
        SAFE_CALL(cudaMemcpy(d_qy, qy, nq * sizeof(double), cudaMemcpyHostToDevice));
        SAFE_CALL(cudaMemcpy(d_qz, qz, nq * sizeof(cucomplex_t), cudaMemcpyHostToDevice));
        SAFE_CALL(cudaMemcpy(d_triangles, triangles, num_triangles * sizeof(triangle_t), cudaMemcpyHostToDevice));



        // number of cuda threads
        int num_threads = 256;
        int num_blocks = nq % num_threads ? nq/num_threads+1 : nq/num_threads;

        // Kernel 1
        ff_tri_kernel1 <<< num_blocks, num_threads >>> (
                nq, d_qx, d_qy, d_qz, 
                num_triangles, d_triangles, rot, d_ff);
        SAFE_CALL(cudaGetLastError());

        // allocate memory to computed ff
        SAFE_CALL(cudaMemcpy(ff, d_ff, nq * sizeof(cucomplex_t), cudaMemcpyDeviceToHost));
 
        cudaFree(d_triangles);
        cudaFree(d_qz);
        cudaFree(d_qy);
        cudaFree(d_qx);
        cudaFree(d_ff);
    } 
}

