# include "patchAverage/patchAverage.H"
# include "pyBlockMesh/pyBlockMesh.H"
# include "fvCFDWrapper/fvCFDWrapper.H"
# include "utils/argumentParser.H"
// include standard library
# include <pybind11/pybind11.h>
# include <pybind11/stl.h>
# include "fvCFD.H"

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

    //py::class_<Foam::IOdictionary>(m, "IOdictionary")
    //.def(py::init<const Foam::word&>());


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
	.def(py::init<const fvCFDWrapper&>())
	.def("calculatePatchAverage", &patchAverage::calculateAverage)
	.def("__repr__", [](const patchAverage& pa) {
	    std::string ret = "<patchAverage>";
	    return ret;
	});

    //bindPyBlockMesh(m);
    py::class_<pyBlockMesh>(m, "blockMesh")
    .def(py::init<const fvCFDWrapper&>())
    .def("generateMesh", &pyBlockMesh::generateMesh)
    .def("__repr__", [](const pyBlockMesh& bm) {
            std::string ret = "<blockMesh>";
            return ret;
    });


    
    m.attr("__version__") = "0.0.1";
}
