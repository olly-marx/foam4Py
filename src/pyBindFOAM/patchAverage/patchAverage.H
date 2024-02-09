#ifndef PATCH_AVERAGE_H
#define PATCH_AVERAGE_H

#include "fvCFD.H"
#include "pyBindFOAM/fvCFDWrapper/fvCFDWrapper.H"
#include "pyBindFOAM/utils/importObject.H"
#include "pyBindFOAM/utils/argumentParser.H"
#include <pybind11/pybind11.h>
#include <string>
#include "scalar.H"
#include <vector>

namespace py = pybind11;

class patchAverage {
public:
    patchAverage(const fvCFDWrapper& foamCase);

    ~patchAverage();

    void calculateAverage(py::object pyargv11);

private:
    const fvCFDWrapper& foamCase_;
};

//void bindPatchAverage(py::module &m);

//__attribute__ ((visibility ("default"))) void init_patchAverage(pybind11::module m);
//void init_patchAverage(pybind11::module m);

#endif // PATCH_AVERAGER_H

