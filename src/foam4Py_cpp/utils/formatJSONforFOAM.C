#include "formatJSONforFoam.H"

Foam::word utils::JSONforFoam(nl::json& obj, const nl::json::value_t& valueType, bool NESTED)
{
    std::string result = "";

    if(valueType==nl::json::value_t::array)
    {
        result += "(";
        for(nl::json::iterator it = obj.begin(); it != obj.end(); ++it)
        {
            result += JSONforFoam(it.value(), it.value().type(), true);
            if(it != obj.end()-1)
            {
                result += " ";
            }
        }
        result += ")";
    }
    else if(valueType==nl::json::value_t::object)
    {
        result += "{";
        for(nl::json::iterator it = obj.begin(); it != obj.end(); ++it)
        {
            result += JSONforFoam(it.value(), it.value().type());
            if(it != obj.end()-1)
            {
                result += " ";
            }
        }
        result += "}";
    }
    else if(valueType==nl::json::value_t::string)
    {
        result += obj.dump();
        result.erase(std::remove(result.begin(), result.end(), '\"'), result.end());
    }
    else
    {
        result += obj.dump();
    }
    return result;
}
