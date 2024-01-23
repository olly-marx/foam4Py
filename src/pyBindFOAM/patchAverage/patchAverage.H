#ifndef PATCH_AVERAGE_H
#define PATCH_AVERAGE_H

#include "fvCFD.H"
#include <pybind11/pybind11.h>

class patchAverage {
public:
    patchAverage(const word& fieldName, const word& patchName);

    ~patchAverage();

    void calculateAverage();

private:
    const word& fieldName_;
    const word& patchName_;
};

//__attribute__ ((visibility ("default"))) void init_patchAverage(pybind11::module m);
//void init_patchAverage(pybind11::module m);

#endif // PATCH_AVERAGER_H

