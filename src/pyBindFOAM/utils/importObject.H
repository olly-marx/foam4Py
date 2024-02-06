#include "fvCFD.H"
#include "pyBindFOAM/fvCFDWrapper/fvCFDWrapper.H"

namespace utils
{
/**
 * @brief Imports a dictionary from the given foamCase for the specified objectName.
 *
 * @param foamCase The fvCFDWrapper representing the foamCase.
 * @param objectName The name of the dictionary object to import.
 * @return Foam::dictionary The imported dictionary.
 */
    Foam::dictionary importDictionary(const fvCFDWrapper& foamCase, const std::string& objectName);
    Foam::dictionary makeDict(nl::json& dict);
    void addArray(Foam::dictionary& resultDict, nl::json& array);
}
