#ifndef ARGUMENTPARSER_H
#define ARGUMENTPARSER_H

# include <pybind11/pybind11.h>
# include <iostream>

#if PY_VERSION_HEX < 0x03000000
#define MyPyText_AsString PyString_AsString
#else
#define MyPyText_AsString PyUnicode_AsUTF8
#endif

namespace py = pybind11;

// Class to parse command line arguments
class arguments
{
    public:
        int argc_;
        char** argv_;

        arguments(py::object pyargv11);
};

#endif // ARGUMENTPARSER_H
