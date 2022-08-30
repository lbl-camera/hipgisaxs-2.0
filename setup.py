

import os
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.util import convert_path

# hack to make it work in virtualenv
import sysconfig
cfg = sysconfig.get_config_vars()
pylib = os.path.join(cfg['LIBDIR'], cfg['LDLIBRARY'])
pyinc = cfg['INCLUDEPY']
pyver = cfg['VERSION']

print(pylib)
print(pyinc)

# versioning
main_ns = {}
ver_path = convert_path('gisaxs/_version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


ext = Extension("gisaxs.cHipgisaxs",
        language = 'c++',
        include_dirs = ["src", pyinc],
        extra_compile_args = ['-fopenmp' ],
        extra_link_args = ['-fopenmp' ],
        sources = [
            "src/pyHipgisaxs.cpp",
            "src/ff_tri_cpu.cpp"
            ]
        )

setup(name='gisaxs',
      author ='Dinesh Kumar',
      version = main_ns['__version__'],
      description = "Companian C++ library for HipGISAXS-2.0 package developed by CAMERA/LBL", 
      packages = [ 'gisaxs' ],
      ext_modules = [ ext ]
      )

