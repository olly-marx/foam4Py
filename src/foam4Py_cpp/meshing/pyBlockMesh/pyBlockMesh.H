#ifndef PY_BLOCK_MESH_H
#define PY_BLOCK_MESH_H

#include "fvCFD.H"
#include "fvCFDWrapper.H"
#include "importObject.H"
#include "argumentParser.H"
#include <pybind11/pybind11.h>

#include "Pair.H"
#include "mapPolyMesh.H"
#include "polyTopoChanger.H"
#include "slidingInterface.H"

#include "objectRegistry.H"
#include "foamTime.H"
#include "IOdictionary.H"
#include "IOPtrList.H"

#include "blockMesh.H"
#include "preservePatchTypes.H"
#include "emptyPolyPatch.H"
#include "cellSet.H"

#include "argList.H"
#include "OSspecific.H"
#include "OFstream.H"


namespace py = pybind11;

class pyBlockMesh {
public:
    pyBlockMesh(const fvCFDWrapper& foamCase);

    ~pyBlockMesh();

    void runBlockMesh(py::object pyargv11);

private:
    const fvCFDWrapper& foamCase_;
};

#endif // BLOCK_MESH_H

