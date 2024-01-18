#ifndef PATCH_AVERAGE_H
#define PATCH_AVERAGE_H

#include "fvCFD.H"

class pyBindPatchAverage {
public:
    pyBindPatchAverage(const word& fieldName, const word& patchName);

    ~pyBindPatchAverage();

    void calculateAverages();

private:
    word& fieldName_;
    word& patchName_;
};

#endif // PATCH_AVERAGER_H

