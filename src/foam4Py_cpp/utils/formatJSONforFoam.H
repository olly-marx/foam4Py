#include "fvCFD.H"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

namespace utils
{
    void JSONforFoam(const std::string& key, json& value, std::ostringstream& os, int indent=0);
}

