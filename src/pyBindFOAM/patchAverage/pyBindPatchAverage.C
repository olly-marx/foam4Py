#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "fvCFD.H"

namespace py = pybind11;

#include "patchAverage.H"

PYBIND11_MODULE(pyBindPatchAverage, m) {
    m.doc() = "pyBindPatchAverage Module";

    m.def("calculateAverages", &pyBindPatchAverage::calculateAverages, "Calculate averages of a field");
