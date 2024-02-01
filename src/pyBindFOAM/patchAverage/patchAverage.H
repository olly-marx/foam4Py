#ifndef PATCH_AVERAGE_H
#define PATCH_AVERAGE_H

#include "fvCFD.H"
#include "pyBindFOAM/fvCFDWrapper/fvCFDWrapper.H"
#include <pybind11/pybind11.h>
#include <string>

namespace py = pybind11;

class patchAverage {
public:
    patchAverage(const std::string fieldName, const std::string patchName,
            const fvCFDWrapper& foamCase);


    ~patchAverage();

    void calculateAverage();

private:
    Foam::word fieldName_;
    Foam::word patchName_;
    const fvCFDWrapper& foamCase_;
};

//void bindPatchAverage(py::module &m);

//__attribute__ ((visibility ("default"))) void init_patchAverage(pybind11::module m);
//void init_patchAverage(pybind11::module m);

#endif // PATCH_AVERAGER_H

