#include "formatJSONforFoam.H"

void utils::JSONforFoam(const std::string& key, json& value, std::ostringstream& os, int indent)
{
    std::string indentation(indent, ' ');

    if (key == "")
    {
        if(value.is_object())
        {
            for(json::iterator it = value.begin(); it != value.end(); ++it)
            {
                JSONforFoam(it.key(), it.value(), os, indent+4);
            }
        }
        else if(value.is_array())
        {
            os << indentation << "( ";
            for(json::iterator it = value.begin(); it != value.end(); ++it)
            {
                if(it.value().is_number())
                {
                    os << it.value() << " ";
                }
                else
                {
                    os << "\n" << indentation << it.value();
                }
            }
            os << " )" <<"\n";
        }
        else if (value.is_string())
        {
            // Remove the quotes from the string
            std::string valueStr = value.dump();
            valueStr.erase(std::remove(valueStr.begin(), valueStr.end(), '\"'), valueStr.end());
            os << valueStr << "\n";
        }
        else if (value.is_number())
        {
            os << value << " ";
        }

    }
    else
    {
        os << indentation << key << " ";
        if(value.is_object())
        {
            os << "\n" << indentation << "{" << "\n";
            for(json::iterator it = value.begin(); it != value.end(); ++it)
            {
                JSONforFoam(it.key(), it.value(), os, indent+4);
            }
            os << indentation << "}" << "\n" << "\n";
        }
        else if(value.is_array())
        {
            os << "\n" << indentation << "(" << "\n";
            for(json::iterator it = value.begin(); it != value.end(); ++it)
            {
                JSONforFoam("", it.value(), os, indent+4);
            }
            os << indentation << ");" <<"\n";
        }
        else if (value.is_string())
        {
            std::string valueStr = value.dump();
            valueStr.erase(std::remove(valueStr.begin(), valueStr.end(), '\"'), valueStr.end());
            os << valueStr << ";" << "\n";
        }
        else if (value.is_number())
        {
            os << value << ";" << "\n";
        }
    }
}
