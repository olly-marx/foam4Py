// json_to_dictionary.h
#ifndef JSON_TO_DICTIONARY_H
#define JSON_TO_DICTIONARY_H

#include <fvCFD.H>
#include <nlohmann/json.hpp>
#include "pybind11_json/pybind11_json.hpp"

using json = nlohmann::json;

Foam::dictionary jsonToDictionary(const json& jsonData);

#endif  // JSON_TO_DICTIONARY_H

