
#include <complex.h>

#ifndef HIG_TYPES__H
#define HIG_TYPES__H


namespace hig {

    typedef std::complex<float> complex_t;

    struct vector3_t {
        float x_, y_, z_;

        vector3_t(): x_(0), y_(0), z_(0) {}

        vector3_t(float x, float  y, float z): x_(x), y_(y), z_(z) {}

        float norm() const {
            return (x_ * x_ + y_ * y_ + z_ * z_);
        }

        float abs() const {
            return sqrt(this->norm());
        }

        vector3_t operator+(const vector3_t &v) {
            return vector3_t(x_ + v.x_, y_ + v.y_, z_ + v.z_);
        }

        vector3_t operator-(const vector3_t &v) {
            return vector3_t(x_ - v.x_, y_ - v.y_, z_ - v.z_);
        }

        void operator/=(float s) {
            x_ /= s;
            y_ /= s;
            z_ /= s;
        }
    };

    inline float dot(const vector3_t &v1, const vector3_t &v2) {
        return (v1.x_ * v2.x_ + v1.y_ * v2.y_ + v1.z_ * v2.z_);
    }

    inline complex_t dot(const complex_t *q, vector3_t n) {
        return (q[0] * n.x_ + q[1] * n.y_ + q[2] * n.z_);
    }

    inline vector3_t cross(const vector3_t &v1, const vector3_t &v2) {
        vector3_t rv;
        rv.x_ = v1.y_ * v2.z_ - v1.z_ * v2.y_;
        rv.y_ = v1.z_ * v2.x_ - v1.x_ * v2.z_;
        rv.z_ = v1.x_ * v2.y_ - v1.y_ * v2.x_;
        return rv;
    }

    struct triangle_t {
        vector3_t v1;
        vector3_t v2;
        vector3_t v3;
    };


    inline float norm3(const complex_t *a) {
        return (a[0] * std::conj(a[0]) + 
                a[1] * std::conj(a[1]) +
                a[2] * std::conj(a[2])).real();
    }
}

#endif // HIG_TYPES__H
