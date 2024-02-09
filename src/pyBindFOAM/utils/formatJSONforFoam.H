#include "fvCFD.H"
#include <nlohmann/json.hpp>

namespace nl = nlohmann;

namespace utils
{
    Foam::word JSONforFoam(nl::json& obj, const nl::json::value_t& valueType, bool NESTED=false);
}

