#ifndef FOAMJSON_H
#define FOAMJSON_H

#include "fvCFD.H"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

/**
 * @file foamjson.h
 * @brief Declarations for functions related to converting Foam objects to JSON format.
 */

namespace utils
{
    /**
     * @brief Convert Foam objects to JSON format recursively.
     * 
     * This function recursively converts Foam objects to JSON format.
     * 
     * @param key The key associated with the Foam object.
     * @param value The Foam object to be converted.
     * @param os The output stream to write the JSON representation.
     * @param indent The indentation level for pretty-printing (default is 0).
     */
    void JSONforFoam(const std::string& key, json& value, std::ostringstream& os, int indent = 0);
}

#endif // FOAMJSON_H

