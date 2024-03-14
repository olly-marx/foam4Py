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

/**
 * @file patch_average.h
 * @brief Declarations for the pyPatchAverage class, providing Python bindings for patchAverage utility.
 */

/**
 * @class pyPatchAverage
 * @brief Class providing Python bindings for the patchAverage utility.
 * 
 * This class wraps the patchAverage utility from OpenFOAM and provides Python bindings
 * to enable its use within Python scripts.
 */
class pyPatchAverage {
public:
    /**
     * @brief Constructor for the pyPatchAverage class.
     * 
     * @param foamCase Reference to the fvCFDWrapper containing the Foam case.
     */
    pyPatchAverage(const fvCFDWrapper& foamCase);

    /**
     * @brief Destructor for the pyPatchAverage class.
     */
    ~pyPatchAverage();

    /**
     * @brief Function to run the patchAverage utility.
     * 
     * This function executes the patchAverage utility with the provided command-line arguments.
     * 
     * @param pyargv11 Command-line arguments passed from Python.
     */
    void runPatchAverage(py::object pyargv11);

private:
    const fvCFDWrapper& foamCase_; /**< Reference to the fvCFDWrapper containing the Foam case. */
};

//void bindPatchAverage(py::module &m);

//__attribute__ ((visibility ("default"))) void init_patchAverage(pybind11::module m);
//void init_patchAverage(pybind11::module m);

#endif // PATCH_AVERAGER_H

