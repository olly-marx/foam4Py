#include "pyPatchAverage/pyPatchAverage.H"
#include "pyBlockMesh/pyBlockMesh.H"
#include "fvCFDWrapper/fvCFDWrapper.H"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "fvCFD.H"

namespace py = pybind11;

PYBIND11_MODULE(openfoam_python_api_bindings, m) {
    m.doc() = R"pbdoc(
        openfoam_python_api_bindings
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

    // Bind pyIcoFoam class
    py::class_<pyIcoFoam>(m, "pyIcoFoam")
        .def(py::init<const fvCFDWrapper&>())
        .def("runIcoFoam", &pyIcoFoam::runIcoFoam);

    m.attr("__version__") = "0.0.1";
}

