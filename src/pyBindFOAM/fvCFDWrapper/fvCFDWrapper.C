#include "fvCFDWrapper.H"
#include "pybind11_json/pybind11_json.hpp"
#include <iostream>

// Constructor
fvCFDWrapper::fvCFDWrapper() {
    // Default constructor, you can initialize members here
}

fvCFDWrapper::fvCFDWrapper(const py::dict& dictionaries) :
    caseDictionaries(dictionaries) {}

dictionary fvCFDWrapper::getControlDict() const {
    return controlDict;
}

const json& fvCFDWrapper::getDictionaries() const
{
    return caseDictionaries;
}

// Binding code
// void bindfvCFDWrapper(py::module &m) {
//}
