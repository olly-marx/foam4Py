import io
import os
import re
import sys
from setuptools import setup, find_packages

# Read README.md file for long description
this_directory = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version from _version.py file
VERSIONFILE = "openfoam_interface/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# Extract Python version
v = sys.version_info
py_version = ".".join([str(v.major), str(v.minor), str(v.micro)])

# Set CMake environment variables
if 'MAKEFLAGS' not in os.environ: 
    os.environ['MAKEFLAGS'] = "-j 1"
os.environ['CMAKE_EXPORT_COMPILE_COMMANDS'] = 'ON'

setup(
    name="openfoam_interface",
    version=verstr,
    author='Oliver Marx',
    author_email='oliver.j.marx@gmail.com',
    description='A package that allows the user to use OpenFOAM in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/olly-marx/openfoam_interface',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "scikit-build",
        "cmake",
    ],
    scripts=[
        "bin/openfoam_interface",
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

