#ifndef PATCH_AVERAGE_H
#define PATCH_AVERAGE_H

#include "fvCFD.H"

namespace pyBindFOAM{
    
    class patchAverage {
    public:
	patchAverage(const word& fieldName, const word& patchName);

	~patchAverage();

	void calculateAverages();

    private:
	const word& fieldName_;
	const word& patchName_;
    };

}

#include <pybind11/pybind11.h>
__attribute__((visibility("default"))) void init_patchAverage(pybind11::module m);

#endif // PATCH_AVERAGER_H

