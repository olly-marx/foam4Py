import re
import subprocess
from pathlib import Path

from skbuild import setup  # This line replaces 'from setuptools import setup'
import argparse

import io
import sys, os
this_directory = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

import re
VERSIONFILE="pyBindFOAMPackage/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

v = sys.version_info
py_version = ".".join([str(v.major), str(v.minor), str(v.micro)])
print(py_version)

if 'MAKEFLAGS' not in os.environ: 
    os.environ['MAKEFLAGS'] = "-j 1"

pybind_value='ON'

setup(
    name="pyBindFOAM",
    version=verstr,
    cmake_source_dir='src/',
    include_package_data=True,
    packages=['pyBindFOAMPackage', 'pyBindFOAMPackage.include','src/pybind11'],
    #package_dir={''},
    cmake_args=[
        '-DCMAKE_PYTHON_BINDINGS={}'.format(pybind_value),
        '-DFOAM:BOOL={}'.format('ON'),
        '-DCMAKE_CXX_COMPILER={}'.format('/usr/bin/g++'),
        #'-DCMAKE_BUILD_TYPE={}'.format('Release'),
        # '-DMPI_CXX_COMPILER={}'.format(mpicxx),
        # '-DMPI_C_COMPILER={}'.format(mpicc),
        #'-DMPI:BOOL={}'.format(mpi_value),
        #'-DOPENMP:BOOL={}'.format(openmp_value),
        f'-DCMAKE_PYVERSION={py_version}'
    ],
    author=['Oliver Marx'],
    author_email='oliver.j.marx@gmail.com',
    description='A version of OpenFOAM with a python interface',
    install_requires=[
        "numpy",
        "scikit-build",
        "cmake",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
