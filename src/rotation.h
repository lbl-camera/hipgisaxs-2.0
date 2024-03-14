
#include <cuda.h>

#include "cmplx_utils.cuh"

#include "types.h"

#ifndef ROT_MATRIX__H
#define ROT_MATRIX__H

namespace hig {
    class RotMatrix_t {
        private:
            double data_[9];

        public:
            // constructor 1
            __hstdev__
            RotMatrix_t() {
                data_[0] = 1.;
                data_[1] = 0.;
                data_[2] = 0.;
                data_[3] = 0.;
                data_[4] = 1.;
                data_[5] = 0.;
                data_[6] = 0.;
                data_[7] = 0.;
                data_[8] = 1.;
            }

            // constructor 2
            __hstdev__
            RotMatrix_t(double *a) {
                for (int i = 0; i < 9; i++) data_[i] = a[i];
            }

            // copy constructor
            __hstdev__
            RotMatrix_t(const RotMatrix_t &rhs) {
                for (int i = 0; i < 9; i++) data_[i] = rhs.data_[i];
            }

            // assignment operator
            __hstdev__
            RotMatrix_t operator=(const RotMatrix_t &rhs) {
                for (int i = 0; i < 9; i++) data_[i] = rhs.data_[i];
                return *this;
            }

            __device__ 
            void rotate(const double x, const double y, const cucomplex_t z, 
                    cucomplex_t *v) const {
    
                v[0] = data_[0] * x + data_[1] * y + data_[2] * z;
                v[1] = data_[3] * x + data_[4] * y + data_[5] * z;
                v[2] = data_[6] * x + data_[7] * y + data_[8] * z;
            }
    };
} // namespace hig
#endif // ROT_MATRIX__H
