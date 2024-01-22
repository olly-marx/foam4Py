#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "fvCFD.H"

namespace py = pybind11;

#include "patchAverage.H"

PYBIND11_MODULE(patchAverage, m) {
    m.doc() = "patchAverage Module";

    m.def("calculateAverages", &patchAverage::calculateAverages, "Calculate averages of a field");
}
