#ifndef PATCH_AVERAGE_H
#define PATCH_AVERAGE_H

#include "fvCFD.H"
#include <pybind11/pybind11.h>
#include <string>

class patchAverage {
public:
    patchAverage(const std::string fieldName, const std::string patchName);

    ~patchAverage();

    void calculateAverage();

private:
    Foam::word fieldName_;
    Foam::word patchName_;
};

//__attribute__ ((visibility ("default"))) void init_patchAverage(pybind11::module m);
//void init_patchAverage(pybind11::module m);

#endif // PATCH_AVERAGER_H

