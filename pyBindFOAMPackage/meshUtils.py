from pyBindFOAMPackage import fvCFDWrapper
from pyBindFOAMPackage import patchAverage
import json

def runBlockMesh(project_dir, dictionaries):
    # Run the meshing utility blockMesh
    fvCFD = fvCFDWrapper(dictionaries)

    field = "p"
    patch = "movingWall"

    patchAverageInstance = patchAverage(field, patch, fvCFD)
    patchAverageInstance.calculateAverage()


