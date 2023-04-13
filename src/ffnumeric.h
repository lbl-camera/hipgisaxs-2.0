
#include "cmplx_utils.cuh"
#include "types.h"

#ifndef HIG_TRIANGULATION__H
#define HIG_TRIANGULATION__H

/** Coumpute form-factor of a triangulated volume
 *
 * @param int number of triangles
 * @param triangle_t* pointer to array of triangles
 * @param int number of q-points
 * @param double * array of x-component of q-vectors
 * @param double * array of y-component of q-vectors
 * @param complex * array of z-component of q-vectors
 * @param RotMatrix_t rotation matrix
 * @param complex * array to hold computed form-factor values
 *
 */
namespace hig {
    void FFTriangulation(int,
        const triangle_t *,
        int,
        const double *,
        const double *,
        const cucomplex_t *,
        const RotMatrix_t, 
        cucomplex_t *);
} // namespace hig

#endif // HIG_TRIANGULATION__H
