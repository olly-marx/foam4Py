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

/**
 * @file py_block_mesh.h
 * @brief Declarations for the pyBlockMesh class, which provides Python bindings for the blockMesh utility.
 */

/**
 * @class pyBlockMesh
 * @brief Class providing Python bindings for the blockMesh utility.
 * 
 * This class wraps the blockMesh utility from OpenFOAM and provides Python bindings
 * to enable its use within Python scripts.
 */
class pyBlockMesh {
public:
    /**
     * @brief Constructor for the pyBlockMesh class.
     * 
     * @param foamCase Reference to the fvCFDWrapper containing the Foam case.
     */
    pyBlockMesh(const fvCFDWrapper& foamCase);

    /**
     * @brief Destructor for the pyBlockMesh class.
     */
    ~pyBlockMesh();

    /**
     * @brief Function to run the blockMesh utility.
     * 
     * This function executes the blockMesh utility with the provided command-line arguments.
     * 
     * @param pyargv11 Command-line arguments passed from Python.
     */
    void runBlockMesh(py::object pyargv11);

private:
    const fvCFDWrapper& foamCase_; /**< Reference to the fvCFDWrapper containing the Foam case. */
};

#endif // PY_BLOCK_MESH_H

