cmake_minimum_required(VERSION 3.8)
project(hipgisaxs CXX CUDA) 
set(hipgisaxs_VERSION_MAJOR 2) 
set(hipgisaxs_VERSION_MINOR 0)

#C++ 17 Stuff
set(CMAKE_CXX_STANDARD 17) 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
set(CMAKE_CXX_FLAGS_DEBUG "-DHIPGISAXS_DEBUG ${CMAKE_CXX_FLAGS_DEBUG}")
set(CMAKE_CUDA_STANDARD 17)
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -std=c++17")



set(SRC 
    ${PROJECT_SOURCE_DIR}/src/ff_tri_gpu.cu
    ${PROJECT_SOURCE_DIR}/src/pyTriangulation.cpp
   )

include_directories(${PROJECT_SOURCE_DIR}/src)

# CUDA Stuff
include_directories(${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES})
link_directories(${CMAKE_CUDA_TOOKIT_LIB_DIRECTORIES})
set(CMAKE_CUDA_FLAGS "--default-stream per-thread ${CMAKE_CUDA_FLAGS}")
set(CMAKE_CUDA_FLAGS_DEBUG "-G -DTOMOCAM_DEBUG ${CMAKE_CUDA_FLAGS_DEBUG}")

#python
set(Python_FIND_VIRTUALENV FIRST)
find_package(Python COMPONENTS Interpreter Development REQUIRED) 
include_directories(${Python_INCLUDE_DIRS})

#pybind11
find_package(pybind11 REQUIRED) 
include_directories(${pybind11_INCLUDE_DIR})
option(USING_SETUP_PY "building through setup.py" OFF)
if (USING_SETUP_PY)
    add_definitions(-DUSE_PYBIND11_PRINT)
endif(USING_SETUP_PY)


add_library(meshff MODULE ${SRC})
set_target_properties(meshff PROPERTIES 
                      CXX_VISIBILITY_PRESET "hidden" 
                      PREFIX "${PYTHON_MODULE_PREFIX}" 
                      SUFFIX "${PYTHON_MODULE_EXTENSION}")
target_link_libraries(meshff PRIVATE pybind11::module)
target_link_libraries(meshff PRIVATE ${Python_LIBRARIES})
target_compile_features(meshff PRIVATE cxx_std_17)
set_target_properties(meshff PROPERTIES CUDA_ARCHITECTURES "60;61;62")

#install(TARGETS cuTriangulationFF 
#        ARCHIVE DESTINATION gisaxs
#        LIBRARY DESTINATION gisaxs)
