#include "fvCFD.H"
#include "fvCFDWrapper.H"

namespace utils
{
/**
 * @brief Imports a dictionary from the given foamCase for the specified objectName.
 *
 * @param foamCase The fvCFDWrapper representing the foamCase.
 * @param objectName The name of the dictionary object to import.
 * @return Foam::dictionary The imported dictionary.
 */
    dictionary importDictionary(const fvCFDWrapper& foamCase, const std::string& objectName);
    dictionary makeDict(json& dict);
}
