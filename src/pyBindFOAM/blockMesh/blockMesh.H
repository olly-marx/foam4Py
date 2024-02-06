#ifndef BLOCK_MESH_H
#define BLOCK_MESH_H

#include "fvCFD.H"
#include "pyBindFOAM/fvCFDWrapper/fvCFDWrapper.H"
#include <pybind11/pybind11.h>
#include <string>

namespace py = pybind11;

class blockMesh {
public:
    blockMesh(const fvCFDWrapper& foamCase);

    ~blockMesh();

    void generateMesh();

private:
    const fvCFDWrapper& foamCase_;
};

#endif // BLOCK_MESH_H

