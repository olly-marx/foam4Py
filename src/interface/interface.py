"""
pyBindFOAM

This script/module is part of the pyBindFOAM project, which provides a Python
interface to OpenFOAM C++. It uses the pybind11 library to generate
bindings to the OpenFOAM C++ API.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    This script is the primary user interface to the pyBindFOAM project. It
    provides a command line interface to the various functions and classes
    provided by the pyBindFOAM library.

Usage:
    

Dependencies:
    - Python 3.5+
    - pybind11
    - foam-extend 5.0

License:


For more information and updates, visit:


"""
# The goal of this script is to provide a command line interface to the
# user. It should be able to do the following:
#   - Import a case directory by specifying the path to the case directory
#   - Call a function to convert the default case dictionaries (system/controlDict,
#     system/fvSchemes, system/fvSolution, constant/transportProperties,
#     system/blockMeshDict) to Python dictionaries. Use a edit history file
#     to correctly import the latest version of the dictionaries.
#   - Edit the Python dictionaries, and save the changes to a history file
#   - Run the case by calling a refactored version of blockMesh, and then
#     running a solver (e.g. simpleFoam, pimpleFoam, etc.)
# ------------------------------------------------------------------------------
# Import the required modules
import argparse
import os
import sys
import subprocess
import pyBindFOAMPackage as pbf
import dictionaryTools as dt
# ------------------------------------------------------------------------------
# Define the main function
def main():
    # Start by greeting the user and printing something that makes it clear
    # that we are in the pyBindFOAM interface
    greeting = """
    **********************************************************
    *                                                        *
    *                  Welcome to pyBindFOAM!                *
    *                                                        *
    **********************************************************

    pyBindFOAM is a Python interface to the FOAM (OpenFOAM) C++
    library, enabling you to harness the power of OpenFOAM
    capabilities within a Python environment.

    Key Features:
    - Seamless integration of FOAM functionalities in Python scripts.
    - Access to FOAM classes, solvers, utilities, and more.
    - Combine the flexibility of Python with the robustness of FOAM.

    Getting Started:
    1. Import OpenFOAM project directory.
    2. Write "help" to see a list of available commands.
    """
    print(greeting)
    # Now, we need to define the command line arguments that the user can
    # specify. We will use the import command to import an OpenFOAM project
    # directory.
    while True:
        # The first prompt will be to import an OpenFOAM project directory.
        project_dir = input("Enter the path to the OpenFOAM project directory: ")
        # Check if the directory exists
        if not os.path.isdir(project_dir):
            raise ValueError("The specified directory does not exist.")
            continue
        if not os.path.isfile(os.path.join(project_dir, "system/controlDict")):
            raise ValueError("The specified directory is not a valid OpenFOAM"+\
                    "project. \n no controlDict file found in the system"+\
                    "directory.")
            continue
        if not os.path.isdir(os.path.join(project_dir, "constant")):
            raise ValueError("The specified directory is not a valid OpenFOAM"+\
                    "project. \n no constant directory found.")
        if not os.path.isdir(os.path.join(project_dir, "0")):
            raise ValueError("The specified directory is not a valid OpenFOAM"+\
                    "project. \n no 0 directory found.")
            continue

        break

    # If we get to this point, then we have a valid OpenFOAM project directory.
    # We can now import the project directory into the pyBindFOAM interface.
    controlDict = dt.read_openfoam_dictionary(os.path.join(project_dir, "system/controlDict"))
    print(controlDict)
    


if __name__ == "__main__":
    main()

