#ifndef FVCFDWRAPPER_H
#define FVCFDWRAPPER_H

#include <pybind11/pybind11.h>
#include <nlohmann/json.hpp>
#include "fvCFD.H"

namespace py = pybind11;
using json = nlohmann::json;
using namespace nlohmann;

using namespace pybind11::literals;

/**
 * @brief Wrapper class for interfacing between OpenFOAM's fvCFD library and Python using pybind11.
 */
class fvCFDWrapper {
public:
    /**
     * @brief Default constructor for fvCFDWrapper.
     */
    fvCFDWrapper();

    /**
     * @brief Constructor that takes a Python dictionary and initializes the wrapper.
     *
     * @param dictionaries Python dictionary containing necessary data.
     */
    fvCFDWrapper(const py::dict& dictionaries);

    /**
     * @brief Get the control dictionary from the wrapped fvCFD object.
     *
     * @return Foam::dictionary The control dictionary.
     */
    dictionary getControlDict() const;

    /**
     * @brief Get the case dictionaries from the wrapped fvCFD object.
     *
     * @return const nl::json& The case dictionaries in JSON format.
     */
    const json& getDictionaries() const;

    /**
     * @brief Overloaded assignment operator for fvCFDWrapper.
     *
     * @param other Another instance of fvCFDWrapper to copy from.
     * @return fvCFDWrapper& Reference to the modified instance.
     */
    fvCFDWrapper& operator=(const fvCFDWrapper& other);

private:
    dictionary controlDict;   ///< Control dictionary from fvCFD.
    json caseDictionaries;      ///< Case dictionaries in JSON format.
};

// Binding code
//void bindfvCFDWrapper(py::module &m);

#endif // FVCFDWRAPPER_H
