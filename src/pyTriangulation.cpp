
#include <complex>
#include <vector>
using std::complex;

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/operators.h>

#include "types.h"
#include "rotation.h"
#include "ffnumeric.h"

namespace py = pybind11;

template <typename T>
using np_array_t = py::array_t<T, py::array::c_style | py::array::forcecast>;


template <typename T>
inline T *getPtr(np_array_t<T> array) {
    return (T  *)array.request().ptr;
}

np_array_t<complex<double>> triangulationff_wrapper(
        np_array_t<double> qx, 
        np_array_t<double> qy,
        np_array_t<complex<double>> qz,
        np_array_t<double> rotation_matrix,
        np_array_t<double> vertices) {

    // put mesh information into triangle_t data-structure
    int num_triangles = vertices.shape(0);
    double * v = getPtr(vertices);
    hig::triangle_t * triangles = new hig::triangle_t[num_triangles];
    for (int i = 0; i < num_triangles; i++) {
        int j = 9*i;
        triangles[i].v1 = {v[j  ], v[j+1], v[j+2]};
        triangles[i].v2 = {v[j+3], v[j+4], v[j+5]};
        triangles[i].v3 = {v[j+6], v[j+7], v[j+8]};
    }

    // rotation matrix
    auto rotation = hig::RotMatrix_t(getPtr(rotation_matrix));
    
    // allocate array for form-factor
    int num_q = qx.request().size;
    int ndim = qx.ndim();
    std::vector<ssize_t> shape;
    for (int i = 0; i < ndim; i++) shape.push_back(qx.shape(i));
    auto pyff = np_array_t<complex<double>>(shape);

    // calculate on GPU
    hig::cucomplex_t *tqz =(hig::cucomplex_t *) getPtr(qz);
    hig::cucomplex_t *ff = (hig::cucomplex_t *) getPtr(pyff);
    FFTriangulation(num_triangles, triangles, num_q, 
            getPtr(qx), getPtr(qy), tqz, rotation, ff);
    return pyff;
}

PYBIND11_MODULE(cuTriangulationFF, m) {
    m.doc() = "Python interface to GPU accelerated gisaxs functions";
    m.def("triangulationff", triangulationff_wrapper);
}
