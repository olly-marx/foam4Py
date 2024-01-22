# include <pybind11/pybind11.h>
# include <pybind11/stl.h>
# include <pybind11/numpy.h>
#include "pyBindFOAM/patchAverage/patchAverage.H"

PYBIND11_MODULE(pyBindFOAMMods, m)
{
    m.doc() = "pyBindFOAM: A Python binding for OpenFOAM";

    init_patchAverage(m);
}
