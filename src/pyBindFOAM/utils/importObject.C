#include "importObject.H"
#include "types.H"

Foam::dictionary utils::importDictionary(const fvCFDWrapper& foamCase, const std::string& objectName)
{
    nl::json caseDictionaries = foamCase.getDictionaries();
    std::cout << "caseDictionaries: " << caseDictionaries << std::endl;

    nl::json subDictJson = caseDictionaries[objectName];
    std::cout << "subDictJson: " << subDictJson << std::endl;

    return utils::makeDict(subDictJson);
}

Foam::dictionary utils::makeDict(nl::json& dict)
{
    Foam::dictionary resultDict = Foam::dictionary();

    for(nl::json::iterator it = dict.begin(); it != dict.end(); ++it) {

        Foam::keyType key(Foam::word(it.key()));

        nl::json::value_t val_type = it.value().type();

        std::cout << it.value() << std::endl;

        switch(val_type){
            case nl::json::value_t::object:
                resultDict.add(key, utils::makeDict(it.value()));
                break;
            case nl::json::value_t::array:
                utils::addArray(resultDict, it.value());
                break;
            case nl::json::value_t::string:
                resultDict.add(key, Foam::word(std::string(it.value())));
                break;
            case nl::json::value_t::boolean:
                resultDict.add(key, bool(it.value()));
                break;
            case nl::json::value_t::number_integer:
                resultDict.add(key, int(Foam::scalar(it.value())));
                break;
            case nl::json::value_t::number_unsigned:
                resultDict.add(key, unsigned(Foam::scalar(it.value())));
                break;
            case nl::json::value_t::number_float:
                resultDict.add(key, double(Foam::scalar(it.value())));
                break;
            case nl::json::value_t::null:
                std::cout << "null" << std::endl;
                break;
            default:
                std::cout << "default" << std::endl;
                break;
        }
    }
    return resultDict;
}

void utils::addArray(Foam::dictionary& resultDict, nl::json& subArray)
{
    // Get type of array
    nl::json::value_t val_type = subArray[0].type();
    std::string type;

    if (val_type == nl::json::value_t::object) {
        type = "Foam::dictionary";
    } else if (val_type == nl::json::value_t::array) {
        type = "Foam::List<Foam::scalar>";
    } else if (val_type == nl::json::value_t::string) {
        type = "Foam::word";
    } else if (val_type == nl::json::value_t::boolean) {
        type = "bool";
    } else if (val_type == nl::json::value_t::number_integer) {
        type = "int";
    } else if (val_type == nl::json::value_t::number_unsigned) {
        type = "unsigned";
    } else if (val_type == nl::json::value_t::number_float) {
        type = "double";
    } else {
        type = "void";
        std::cout << "null" << std::endl;
    }

    // Now we can use ResultType to create the list
    using typeName = deduceType
    Foam::List<typeName> list;

    //for (nl::json::iterator it = subArray.begin(); it != subArray.end(); ++it) {

    //    nl::json val = it.value();

    //    switch(val_type){
    //        case nl::json::value_t::object:
    //            resultList.append(utils::makeDict(val));
    //            break;
    //        case nl::json::value_t::array:
    //            Foam::List<Foam::scalar> subList;
    //            utils::addArray(resultDict, it.value());
    //            break;
    //        case nl::json::value_t::string:
    //            list.append(Foam::word(std::string(it.value())));
    //            break;
    //        case nl::json::value_t::boolean:
    //            list.append(bool(it.value()));
    //            break;
    //        case nl::json::value_t::number_integer:
    //            list.append(int(Foam::scalar(it.value())));
    //            break;
    //        case nl::json::value_t::number_unsigned:
    //            list.append(unsigned(Foam::scalar(it.value())));
    //            break;
    //        case nl::json::value_t::number_float:
    //            list.append(double(Foam::scalar(it.value())));
    //            break;
    //        case nl::json::value_t::null:
    //            std::cout << "null" << std::endl;
    //            break;
    //        default:
    //            std::cout << "default" << std::endl;
    //            break;
    //    }
    //}

}

//void utils::addKeyValuePair(Foam::dictionary& resultDict, const Foam::keyType& key, const std::string& val)
//{
//    if (val.find(".") != std::string::npos) {
//        double val_double = stod(val);
//        Foam::scalar val_scalar(val_double);
//        resultDict.add(key, val_scalar);
//    }
//    else if (val.find("yes") != std::string::npos) {
//        bool val_bool = true;
//        resultDict.add(key, val_bool);
//    }
//    else if (val.find("no") != std::string::npos) {
//        bool val_bool = false;
//        resultDict.add(key, val_bool);
//    }
//    else {
//        int val_int = stoi(val);
//        resultDict.add(key, val_int);
//    }
//}
