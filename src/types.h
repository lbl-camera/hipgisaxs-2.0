
#include <complex.h>


#include <cuda.h>
#include <cuda/std/complex>

#ifndef HIG_TYPES__H
#define HIG_TYPES__H
#ifdef __CUDACC__
#define __hstdev__ __host__ __device__
#define __inline_hstdev__ __inline__ __host__ __device__
#else
#define __hstdev__
#define __inline_hstdev__
#define __device__
#endif

namespace hig {
    struct vector3_t {
        double x_, y_, z_;

        __hstdev__
        vector3_t(): x_(0), y_(0), z_(0) {}

        __hstdev__
        vector3_t(double x, double  y, double z): x_(x), y_(y), z_(z) {}

        __hstdev__
        double norm() const {
            return (x_ * x_ + y_ * y_ + z_ * z_);
        }

        __hstdev__
        double abs() const {
            return sqrt(this->norm());
        }

        __hstdev__ 
        vector3_t operator+(const vector3_t &v) {
            return vector3_t(x_ + v.x_, y_ + v.y_, z_ + v.z_);
        }

        __hstdev__
        vector3_t operator-(const vector3_t &v) {
            return vector3_t(x_ - v.x_, y_ - v.y_, z_ - v.z_);
        }

        __hstdev__
        void operator/=(double s) {
            x_ /= s;
            y_ /= s;
            z_ /= s;
        }
    };

    __inline_hstdev__
    double dot(const vector3_t &v1, const vector3_t &v2) {
        return (v1.x_ * v2.x_ + v1.y_ * v2.y_ + v1.z_ * v2.z_);
    }

    __inline_hstdev__
    vector3_t cross(const vector3_t &v1, const vector3_t &v2) {
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
}

#endif // HIG_TYPES__H
