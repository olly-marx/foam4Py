#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <string>
#include <nlohmann/json.hpp>
#include "fvCFD.H"

namespace py = pybind11;
namespace nl = nlohmann;

using namespace pybind11::literals;

class fvCFDWrapper {
public:
    fvCFDWrapper();
    fvCFDWrapper(const py::dict& dictionaries);

    Foam::dictionary getControlDict() const;

    //overload the = operator
    fvCFDWrapper& operator=(const fvCFDWrapper& other);

private:
    Foam::dictionary controlDict;
};

// Binding code
//void bindfvCFDWrapper(py::module &m);

