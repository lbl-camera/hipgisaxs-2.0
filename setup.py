
import os
import subprocess
import logging
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.util import convert_path
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

# hack to make it work in virtualenv
import sysconfig
cfg = sysconfig.get_config_vars()
pylib = os.path.join(cfg['LIBDIR'], cfg['LDLIBRARY'])
pyinc = cfg['INCLUDEPY']
pyver = cfg['VERSION']

# logging
logging.basicConfig()
log = logging.getLogger(__file__)
ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError, IOError, SystemExit)


class CMakeExtension(Extension):
    """
    setuptools.Extension for cmake
    """
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuildExt(build_ext):
    """
    setuptools build_exit which builds using cmake & make
    You can add cmake args with the CMAKE_COMMON_VARIABLES environment variable
    """
    def build_extension(self, ext):
        if isinstance(ext, CMakeExtension):
            output_dir = os.path.abspath(
                os.path.dirname(
                    self.get_ext_fullpath(ext.name)))

            build_type = 'Debug' if self.debug else 'Release'
            cmake_args = ['cmake',
                          ext.sourcedir,
                          '-DUSING_SETUP_PY:BOOL=ON',
                          '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + output_dir,
                          '-DCMAKE_BUILD_TYPE=' + build_type,
                          '-DPYBIND11_PYTHON_VERSION=' + pyver,
                          '-DPYTHON_LIBRARY=' + pylib,
                          '-DPYTHON_INCLUDE_DIR=' + pyinc
                         ]
            cmake_args.extend([x for x in os.environ.get('CMAKE_COMMON_VARIABLES', '').split(' ') if x])

            env = os.environ.copy()
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)
            subprocess.check_call(cmake_args, cwd=self.build_temp, env=env)
            subprocess.check_call(['make', '-j'], cwd=self.build_temp, env=env)
            print()
        else:
            super().build_extension(ext)

# versioning
main_ns = {}
ver_path = convert_path('hipgisaxs/_version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


attrs = {
    'name': 'hipgisaxs', 
    'author': 'Dinesh Kumar',
    'version': main_ns['__version__'],
    'description': 'GIS Simulator',
    'packages': 'hipgisaxs',
    'license': 'HipGISAXS v2.0 License',
    'packages': ['hipgisaxs'],
} 


try:
    ext_attrs = { 'ext_modules': [CMakeExtension('hipgisaxs.ff.meshff', os.getcwd())],
                  'cmdclass': {'build_ext': CMakeBuildExt}
    }
    kwargs = attrs.copy()
    kwargs.update(ext_attrs) 
    setup(**kwargs)
except ext_errors as ex:
    log.warn(ex)
    log.warn('CUDA Extension was not complied. Tyring without the extension')
    setup(**attrs)
    log.info('HipGISAXS was installed without CUDA Extensions. If you think this is mistake, check logfiles and fix errors.')
