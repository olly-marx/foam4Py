# include "patchAverage/patchAverage.H"
// include standard library
# include <iostream>
# include <string>
# include <pybind11/pybind11.h>
# include "fvCFD.H"

namespace py = pybind11;

PYBIND11_MODULE(pyBindFOAMMods, m)
{
    m.doc() = R"pbdoc(
		pyBindFOAMMods module
		-----------------------

		.. currentmodule:: pyBindFOAMMods

		.. autosummary::
		   :toctree: _generate

		   patchAverage
	)pbdoc";

    // Bind patchAverage class to python
    py::class_<patchAverage>(m, "patchAverage")	
	.def(py::init<const std::string, const std::string>())
	.def("calculateAverage", &patchAverage::calculateAverage)
	.def("__repr__", [](const patchAverage& pa) {
	    std::string ret = "<patchAverage>";
	    return ret;
	});

    // Bind word class to python
    py::class_<Foam::word>(m, "word")
    .def(py::init<const char*>())
    .def("__repr__", [](const Foam::word& w) {
		std::string ret = "<word>";
		return ret;
	});

    // Bind the keyType class to python only bind the add method that
    py::class_<Foam::string::keyType>(m, "keyType")
	.def(py::init<const Foam::word&>())

    // Bind dictionary class to python, only bind the default constructor
    // and the overloaded add method with the following signature:
    // Foam::dictionary::add(const keyType&, const word&, bool overwrite = false);
    py::class_<Foam::dictionary>(m, "dictionary")
	.def(py::init())
	.def("add", [](Foam::dictionary& d, const Foam::string::keyType& key, 
		    const Foam::word& word, bool overwrite) {
	    d.add(key, word, overwrite);
    
    
    m.attr("__version__") = "0.0.1";
}
