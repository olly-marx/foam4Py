#include "importObject.H"
#include "formatJSONforFoam.H"

dictionary utils::importDictionary(const fvCFDWrapper& foamCase, const std::string& objectName)
{
    std::cout << "importDictionary" << std::endl;
    nl::json caseDictionaries = foamCase.getDictionaries();

    nl::json subDictJson = caseDictionaries[objectName];
    std::cout << "subDictJson: " << subDictJson << std::endl;

    return utils::makeDict(subDictJson);
}

dictionary utils::makeDict(nl::json& dict)
{
    dictionary resultDict = dictionary();

    std::cout << "makeDict" << std::endl;
    std::cout << dict << std::endl;

    for(nl::json::iterator it = dict.begin(); it != dict.end(); ++it) {

        keyType key(word(it.key()));

        std::cout << it.value() << std::endl;

        nl::json::value_t valueType = it.value().type();

        if(valueType==nl::json::value_t::object)
        {
            resultDict.add(key, utils::makeDict(it.value()));
        }
        else if(valueType==nl::json::value_t::number_integer
            || valueType==nl::json::value_t::number_unsigned)
        {
            scalar value = it.value();
            resultDict.add(key, int(value));
        }
        else if(valueType==nl::json::value_t::number_float)
        {
            scalar value = it.value();
            resultDict.add(key, value);
        }
        else if(valueType==nl::json::value_t::boolean)
        {
            word value = it.value();
            resultDict.add(key, value);
        }
        else
        {
            word value = word(utils::JSONforFoam(it.value(), valueType));
            value.erase(std::remove(value.begin(), value.end(), '\"'), value.end());

            std::cout << "value: " << value << std::endl;
            resultDict.add(key, value);
        }
    }
    return resultDict;
}
