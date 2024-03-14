#include "pyPatchAverage.H"
#include "pyBlockMesh.H"
#include "fvCFDWrapper.H"

#include <pybind11/pybind11.h>
#include "fvCFD.H"

namespace py = pybind11;

PYBIND11_MODULE(foam4Py_module, m) {
    m.doc() = R"pbdoc(
        py4Foam_module
        ---------------------------

        This module provides bindings for interacting with OpenFOAM data.
    )pbdoc";

    // Define __all__ to specify exported symbols
    m.attr("__all__") = py::make_tuple("fvCFDWrapper", "pyPatchAverage", "pyBlockMesh");

    // Bind fvCFDWrapper class
    py::class_<fvCFDWrapper>(m, "fvCFDWrapper")
        .def(py::init<const py::dict&>());

    // Bind pyPatchAverage class
    py::class_<pyPatchAverage>(m, "pyPatchAverage")
        .def(py::init<const fvCFDWrapper&>())
        .def("runPatchAverage", &pyPatchAverage::runPatchAverage);

    // Bind pyBlockMesh class
    py::class_<pyBlockMesh>(m, "pyBlockMesh")
        .def(py::init<const fvCFDWrapper&>())
        .def("runBlockMesh", &pyBlockMesh::runBlockMesh);

    py::class_<dictionary>(m, "dictionary")
        .def(py::init<const dictionary&>());
        //.def("runIcoFoam", &dictionary::runIcoFoam);

    m.attr("__version__") = "0.0.1";
}

