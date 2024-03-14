# __init__.py

"""
OpenFOAM Interface Package

A package containing scripts and modules for the pyBindFOAM interface.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    This package contains various scripts and modules used by the pyBindFOAM interface.
    It includes functionality for importing OpenFOAM dictionaries, editing dictionaries,
    running meshing and post-processing utilities, and more.

Dependencies:
    - Python 3.5+
    - pybind11
    - foam-extend 5.0

"""

# Import necessary modules and scripts
from .openfoam_interface import InterfaceState
from . _version import __version__

# List of scripts and modules to be imported when using "from pyBindFOAMPackage import *"
__all__ = [
    'InterfaceState',
]

