
### openfoam_interface

## Description

openfoam_interface is a Python package that provides a high-level interface to OpenFOAM,
leveraging foam4Py for OpenFOAM interaction. It simplifies the usage of OpenFOAM
functionality without needing to delve into the details of the OpenFOAM C++ library.

## Installation

You can install openfoam_interface from source:

```bash
cd foam4Py
python3 setup.py build && python3 setup.py install
cd ../openfoam_interface
pip install .
```

To verify your installation you can run the test suite:
```bash
openfoam_interface -test
```

## Usage

Once installed, you can use openfoam_interface to perform various tasks related to OpenFOAM simulations. The interface provides easy-to-use functions to set up simulations, run them, and analyze results. Refer to the documentation or source code for detailed usage instructions.
