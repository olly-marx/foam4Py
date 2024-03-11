#ifndef PATCH_AVERAGE_H
#define PATCH_AVERAGE_H

#include "fvCFD.H"
#include "fvCFDWrapper.H"
#include "importObject.H"
#include "argumentParser.H"
#include <pybind11/pybind11.h>
#include <string>
#include "scalar.H"
#include <vector>

namespace py = pybind11;

class pyPatchAverage {
public:
    pyPatchAverage(const fvCFDWrapper& foamCase);

    ~pyPatchAverage();

    void runPatchAverage(py::object pyargv11);

private:
    const fvCFDWrapper& foamCase_;
};

//void bindPatchAverage(py::module &m);

//__attribute__ ((visibility ("default"))) void init_patchAverage(pybind11::module m);
//void init_patchAverage(pybind11::module m);

#endif // PATCH_AVERAGER_H

