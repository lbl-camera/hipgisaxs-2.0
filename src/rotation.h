
#ifndef ROT_MATRIX__H
#define ROT_MATRIX__H

namespace hig {
    class RotMatrix_t {
        private:
            float data_[9];

        public:
            // constructor 1
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
            RotMatrix_t(float *a) {
                for (int i = 0; i < 9; i++) data_[i] = a[i];
            }

            // copy constructor
            RotMatrix_t(const RotMatrix_t &rhs) {
                for (int i = 0; i < 9; i++) data_[i] = rhs.data_[i];
            }

            // assignment operator
            RotMatrix_t operator=(const RotMatrix_t &rhs) {
                for (int i = 0; i < 9; i++) data_[i] = rhs.data_[i];
                return *this;
            }

            void rotate(const float x, const float y, const complex_t z, 
                    complex_t *v) const {
    
                v[0] = data_[0] * x + data_[1] * y + data_[2] * z;
                v[1] = data_[3] * x + data_[4] * y + data_[5] * z;
                v[2] = data_[6] * x + data_[7] * y + data_[8] * z;
            }
    };
} // namespace hig
#endif // ROT_MATRIX__H
