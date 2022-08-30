
#include "types.h"

#ifndef HIG_HIPGISAXS__H
#define HIG_HIPGISAXS__H

/** Coumpute form-factor of a triangulated volume
 *
 * @param int number of triangles
 * @param triangle_t* pointer to array of triangles
 * @param int number of q-points
 * @param float * array of x-component of q-vectors
 * @param float * array of y-component of q-vectors
 * @param complex * array of z-component of q-vectors
 * @param RotMatrix_t rotation matrix
 * @param complex * array to hold computed form-factor values
 *
 */
namespace hig {
    void FFTriangulation(int,
        const triangle_t *,
        int,
        const float *,
        const float *,
        const complex_t *,
        const RotMatrix_t, 
        complex_t *);
} // namespace hig

#endif
