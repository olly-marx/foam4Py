// json_to_dictionary.cpp
#include "convertJSONtoFoamDict.H"

Foam::dictionary jsonToDictionary(const json& jsonData) {
    Foam::dictionary foamDict;

    //try {
    //    pybind11::object pyDict = pybind11::module::import("json").attr("loads")(jsonData.dump());
    //    pybind11::dict pyFoamDict = pyDict.cast<pybind11::dict>();

    //    for (auto it : pyFoamDict) {
    //        std::string key = it.first.cast<std::string>();
    //        std::string value = it.second.cast<std::string>();
    //        foamDict.addEntry(key, value);
    //    }
    //} catch (const std::exception& e) {
    //    // Handle exceptions if needed
    //    Foam::ErrorInFunction << "Error converting JSON to Foam dictionary: " << e.what() << Foam::End;
    //}

    return foamDict;
}

