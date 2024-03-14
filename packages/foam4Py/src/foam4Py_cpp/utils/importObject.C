#include "IStringStream.H"
#include "importObject.H"
#include "formatJSONforFoam.H"

dictionary utils::importDictionary(const fvCFDWrapper& foamCase, const std::string& objectName)
{
    json caseDictionaries = foamCase.getDictionaries();

    std::string objectNameReplaced = objectName;
    std::replace(objectNameReplaced.begin(), objectNameReplaced.end(), '/', '.');

    json subDictJson = caseDictionaries[objectNameReplaced];
    return utils::makeDict(subDictJson);
}

dictionary utils::makeDict(json& dict)
{
    std::ostringstream os("");
    utils::JSONforFoam("", dict, os, 0);
    IStringStream is(os.str());
    dictionary resultDict(is);

    return resultDict;
}
