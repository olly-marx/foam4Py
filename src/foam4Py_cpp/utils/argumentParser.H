#ifndef ARGUMENTPARSER_H
#define ARGUMENTPARSER_H

#include <pybind11/pybind11.h>
#include <iostream>

/**
 * @file argumentparser.h
 * @brief Definition of the arguments class for parsing command line arguments from Python to C++.
 */

#if PY_VERSION_HEX < 0x03000000
#define MyPyText_AsString PyString_AsString
#else
#define MyPyText_AsString PyUnicode_AsUTF8
#endif

namespace py = pybind11;

/**
 * @brief Class to parse command line arguments.
 */
class arguments
{
public:
    /**
     * @brief Get the number of command line arguments.
     * @return The number of command line arguments.
     */
    int argc_;

    /**
     * @brief Get the command line arguments.
     * @return The command line arguments.
     */
    char** argv_;

    /**
     * @brief Constructor for the arguments class.
     * @param pyargv11 A pybind11 object representing the command line arguments.
     */
    arguments(py::object pyargv11);
};

#endif // ARGUMENTPARSER_H

