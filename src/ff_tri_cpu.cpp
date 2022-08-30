#include <iostream>
#include <complex>

#include "types.h"
#include "rotation.h"

namespace hig {

    // constants
    const float TINY = 1.0E-20;
    const complex_t j1 = 1j;
    const complex_t jn = -1j;

    complex_t cpu_triangle_ff (const triangle_t & tri, const complex_t * q){

        // initialize stuff
        complex_t ff = 0;

        // calculate q^2
        float q_sq = norm3(q);

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
        float  t_area = 0.5 * n_t.abs();
        n_t /= 2 * t_area;
 
        // dot (q, n_t)
        complex_t q_dot_nt = dot(q, n_t);

        // calculate projection of q in triangle-plane
        float proj_tq = q_sq - std::norm(q_dot_nt);

        // CASE 1
        if (std::abs(proj_tq) < TINY){
            complex_t q_dot_v = dot(q, vertex[0]);

            // calculate Form-Factor
            ff = j1 * q_dot_nt * t_area / q_sq * std::exp(jn * q_dot_v);
        } else {

            // iterate on each edge :
            for (int e = 0; e < 3; e++) {

                // edge normal
                vector3_t n_e = cross(edge[e], n_t);
                n_e /= n_e.abs(); // normalize

                // dot(q, n_e)
                complex_t q_dot_ne = dot(q, n_e);

                // proj_ne
                float proj_eq = proj_tq - std::norm(q_dot_ne);

                // CASE 2
                if (std::abs(proj_eq) < TINY){

                    // q_dot_v
                    complex_t q_dot_v = dot(q, vertex[e]);

                    // calculate contribution of edge
                    float f0 = edge[e].abs() / (q_sq * proj_tq);
                    complex_t f1 = - q_dot_nt * q_dot_ne;
                    complex_t f2 = std::exp(jn * q_dot_v);
                    ff += (f0 * f1 * f2);
                } else {
                    // CASE 3 (General case)
                    int e1 = (e+1) % 3;
                    float f0 = q_sq * proj_tq * proj_eq;
                    complex_t f1 = jn * q_dot_nt * q_dot_ne;
                    complex_t f2 = dot(q, edge[e]) / edge[e].abs();
                    complex_t t1 = dot(q, vertex[e]);
                    complex_t f3 = std::exp(jn * t1);
                    complex_t t2 = dot(q, vertex[e1]);
                    complex_t f4 = std::exp(jn * t2);
                    ff += f1 * f2 * (f3-f4) / f0;
                }
            }
        }
        return ff;
    }


    /**
     * The function called from outside, as part of the API for a single node.
     */
    void FFTriangulation(
                int num_triangles, const triangle_t * triangles,
                int num_q, const float * qx, const float * qy, 
                const complex_t * qz, const RotMatrix_t rot,
                complex_t *ff) { 
      
        #pragma omp parallel for
        for (int i = 0; i < num_q; i++) {
            complex_t mq[3];
            rot.rotate(qx[i], qy[i], qz[i], mq);
            for (int j = 0; j < num_triangles; j++)
                ff[i] += cpu_triangle_ff(triangles[j], mq);

        }
    }
}

