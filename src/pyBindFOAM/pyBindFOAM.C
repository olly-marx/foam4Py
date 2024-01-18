#include "pyBindFOAM/patchAverage/patchAverage.H"

PYBIND11_MODULE(pyBindFOAM, m)
{
    m.doc() = "pyBindFOAM: A Python binding for OpenFOAM";

    init_patchAverage(m);
}
