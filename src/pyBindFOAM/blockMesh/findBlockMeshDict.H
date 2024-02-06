
autoPtr<Foam::dictionary> meshDictPtr;

{

    meshDictPtr = autoPtr<IOdictionary>(new IOdictionary(meshDictIO));
}

const dictionary& meshDict = meshDictPtr;

