# include "pyBindFOAM/patchAverage/patchAverage.H"

PYBIND11_MODULE(pyBindFOAMMods, m)
{
    m.doc() = "pyBindFOAM: A Python binding for OpenFOAM";

    init_patchAverage(m);
}
