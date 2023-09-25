#include <array>
#include <execution>
#include <complex>

template <typename T>
std::complex<T> coneff(const std::array<T> &qx,
    const std::array<T> &qy,
    const std::array<T> &qz,
    T R0, T R1, T h,
    const std::array<T> &rotation) {

    // find-angle
    T tan_a;
    std::array<T, qx.size()> qp;
    std::transform(std::execution::par_unseq,
        qx.begin(), qx.end(), qy.begin(), qp.begin(),
        [](T x, T y) { return (x * x + y * y); })
}
