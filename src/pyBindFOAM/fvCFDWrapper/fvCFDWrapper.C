#ifndef FVCFDWRAPPER_H
#define FVCFDWRAPPER_H

#include "fvCFDWrapper.H"
#include "pybind11_json/pybind11_json.hpp"
#include <iostream>

// Constructor
fvCFDWrapper::fvCFDWrapper() {
    // Default constructor, you can initialize members here
}

fvCFDWrapper::fvCFDWrapper(const py::dict& dictionaries) {
    // Upon creation of the wrapper we just want to implement time.
    // The mesh is not needed for the time being.

    const nl::json caseDictionaries = dictionaries;

    // We will create a json from the value of the controlDict key
    nl::json controlDictJson = caseDictionaries["controlDict"];

    std::cout << "controlDictJson: " << controlDictJson << std::endl;

    for(nl::json::iterator it = controlDictJson.begin(); it != controlDictJson.end(); ++it) {

        std::cout << "Iterating over controlDictJson" << std::endl;
        Foam::keyType key(Foam::word(it.key()));
        std::string val = it.value();
        Info << "key: " << key << " val: " << val << endl;
        // Try to cast the value to a Foam::Scalar
        // If it fails, just add the word
        try {
            if (val.find(".") != std::string::npos) {
                double val_double = stod(val);
                Foam::scalar val_scalar(val_double);
                controlDict.add(key, val_scalar);
            }
            else if (val.find("yes") != std::string::npos) {
                bool val_bool = true;
                controlDict.add(key, val_bool);
            }
            else if (val.find("no") != std::string::npos) {
                bool val_bool = false;
                controlDict.add(key, val_bool);
            }
            else {
                int val_int = stoi(val);
                controlDict.add(key, val_int);
            }
            // print the type of the key and value
            std::cout << "key: " << typeid(key).name() << std::endl;
            std::cout << "val: " << typeid(controlDict.lookup(key)).name() << std::endl;
        } catch (std::exception& e) {
            std::cout << "Exception: " << e.what() << std::endl;
            controlDict.add(key, val);
        }


    }


    // Add the dictionary to the controlDict
    //controlDict.add(it.key(), dict, true);
}

Foam::dictionary fvCFDWrapper::getControlDict() const {
    return controlDict;
}

// Binding code
// void bindfvCFDWrapper(py::module &m) {
//}

#endif // FVCFDWRAPPER_H
