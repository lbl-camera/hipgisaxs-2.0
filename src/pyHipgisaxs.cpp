
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/operators.h>

#include "types.h"
#include "rotation.h"
#include "hipgisaxs.h"

namespace py = pybind11;

template <typename T>
using np_array_t = py::array_t<T, py::array::c_style | py::array::forcecast>;


template <typename T>
inline T *getPtr(np_array_t<T> array) {
    return (T  *)array.request().ptr;
}

np_array_t<hig::complex_t> triangulationff_wrapper(
        np_array_t<float> qx, np_array_t<float> qy,
        np_array_t<hig::complex_t> qz,
        np_array_t<float> rotation_matrix,
        np_array_t<float> vertices) {

    // put mesh information into triangle_t data-structure
    int num_triangles = vertices.shape(0);
    float * v = getPtr(vertices);
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
    auto pyff = np_array_t<hig::complex_t>(shape);

    // calculate 
    hig::complex_t *tqz =(hig::complex_t *) getPtr(qz);
    hig::complex_t *ff = (hig::complex_t *) getPtr(pyff);
    FFTriangulation(num_triangles, triangles, num_q, 
            getPtr(qx), getPtr(qy), tqz, rotation, ff);
    return pyff;
}

PYBIND11_MODULE(cHipgisaxs, m) {
    m.doc() = "Python interface to Mulit-threaded gisaxs functions";
    m.def("triangulationff", triangulationff_wrapper);
}
