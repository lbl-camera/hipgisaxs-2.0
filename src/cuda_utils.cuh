
#include <cuda.h>
#include <stdio.h>

#ifndef HIG_CUDA_UTILS__H
#define HIG_CUDA_UTILS__H

namespace hig {

#define SAFE_CALL(ans) { gpuAssert((ans), __FILE__, __LINE__); }
    inline void gpuAssert(
        cudaError_t code, const char *file, int line, bool abort = true) {
        if (code != cudaSuccess) {
            fprintf(stderr,
                "GPUassert: %s %s %d\n",
                cudaGetErrorString(code), file, line);
            if (abort) exit(code);
        }
    }
} // namespace hig

#endif // HIG_CUDA_UTILS__H
