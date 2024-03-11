# __init__.py

"""
foam4Py Package

This package contains OpenFOAM modules that have been wrapped using pybind11. The
package allows OpenFOAM functionality to be accessed from Python.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    The foam4Py package contains a number of OpenFOAM modules that have been
    wrapped using pybind11. The package allows OpenFOAM functionality to be
    accessed from Python. The package is designed to be used with foam-extend
    5.0 and Python 3.5+.

Dependencies:
    - Python 3.5+
    - pybind11
    - foam-extend 5.0

"""

# Import necessary modules and scripts
from foam4Py import *
from . _version import __version__

__all__ = [
]

