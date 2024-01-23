# include "patchAverage/patchAverage.H"
// include standard library
# include <iostream>
# include <string>
# include <pybind11/pybind11.h>

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

    py::class_<patchAverage>(m, "patchAverage")	
	.def(py::init<const word&, const word&>())
	.def("calculateAverage", &patchAverage::calculateAverage)
	.def("__repr__", [](const patchAverage& pa) {
	    std::string ret = "<patchAverage>";
	    return ret;
	});
    
    m.attr("__version__") = "0.0.1";
}
