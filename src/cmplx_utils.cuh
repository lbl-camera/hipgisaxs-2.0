
#include <cuda/std/complex>

#include "types.h"

#ifndef CMPLX_UTILS__H
#define CMPLX_UTILS__H
namespace hig {

    typedef cuda::std::complex<double> cucomplex_t;
    using cuda::std::conj;

    __inline_hstdev__ cucomplex_t make_cucomplex(double a, double b) {
        return cucomplex_t(a, b);
    }

    __inline_hstdev__ cucomplex_t dot(const cucomplex_t *a, const vector3_t v) {
        return (a[0] * v.x_ + a[1] * v.y_ + a[2] * v.z_);
    }

    __inline_hstdev__ double norm3(const cucomplex_t *a) {
        return (a[0] * conj(a[0]) + 
                a[1] * conj(a[1]) + 
                a[2] * conj(a[2])).real();
    }
} // namespace hig

#endif // CMPLX_UTILS__H
