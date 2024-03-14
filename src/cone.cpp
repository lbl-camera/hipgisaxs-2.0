#include <vector>
#include <execution>
#include <complex>

template <typename T>
std::vector<complex<T>> coneff(const vector<T> &qx,
    const std::vector<T> &qy,
    const std::vector<T> &qz,
    T R, T H, T Angle,
    const std::vector<T> &rotation) {

    // side-angle
    T tan_a = std::tan(Angle);
    auto rh = R - H / tan_a;
    if (rh < 0) throw "exception: illeagal angle";

    // form rotation matrix
    //
    std::vector<complex<T>> ff;

    for (int i = 0; i < nq; i++) {
        auto qp = std::sqrt(qx[i]*qx[i] + qy[i]*qy[i]);
        auto qv = qz[i] * tan_a;

        ff[i] = inegrate(fn, params, R, rh);
