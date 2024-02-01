# include "patchAverage/patchAverage.H"
# include "fvCFDWrapper/fvCFDWrapper.H"
// include standard library
# include <pybind11/pybind11.h>
# include <pybind11/stl.h>
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

    // Bind word class to python
    py::class_<Foam::word>(m, "word")
    .def(py::init<const char*>())
    .def("__repr__", [](const Foam::word& w) {
		std::string ret = "<word>";
		return ret;
	});

    // Bind the keyType class to python only bind the add method that
    py::class_<Foam::keyType>(m, "keyType")
	.def(py::init<const Foam::word&>());

    // Bind dictionary class to python, only bind the default constructor
    // and the overloaded add method with the following signature:
    // Foam::dictionary::add(const keyType&, const word&, bool overwrite = false);
    py::class_<Foam::dictionary>(m, "dictionary")
	.def(py::init())
	.def("add", [](Foam::dictionary& d, const Foam::keyType& key, 
		    const Foam::word& word, bool overwrite) {
	    d.add(key, word, overwrite);
	});

    //bindfvCFDWrapper(m);
    py::class_<fvCFDWrapper>(m, "fvCFDWrapper")
        .def(py::init<const py::dict&>())
        .def("getControlDict", &fvCFDWrapper::getControlDict)
        //.def("setValue", &fvCFDWrapper::setValue)
        //.def("getValue", &fvCFDWrapper::getValue);
	.def("__repr__", [](const Foam::word& w) {
		std::string ret = "<word>";
		return ret;
	});

    //bindPatchAverage(m);
    py::class_<patchAverage>(m, "patchAverage")	
	.def(py::init<const std::string, const std::string, const fvCFDWrapper&>())
	.def("calculateAverage", &patchAverage::calculateAverage)
	.def("__repr__", [](const patchAverage& pa) {
	    std::string ret = "<patchAverage>";
	    return ret;
	});

    // bind the standard library string class to python
    py::class_<std::string>(m, "string")
	.def(py::init<>())
	.def(py::init<const char*>())
	.def("__repr__", [](const std::string& s) {
	    std::string ret = "<string>";
	    return ret;
	});
    
    
    m.attr("__version__") = "0.0.1";
}
