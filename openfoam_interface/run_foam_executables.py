import os
from foam4Py import fvCFDWrapper
from foam4Py import pyBlockMesh
from foam4Py import pyPatchAverage
from .openfoam_dict_finder import *

def runBlockMesh(project_dir, dictionaries, args):
    # Run the meshing utility blockMesh
    fvCFD = fvCFDWrapper(dictionaries)

    # Run blockMesh
    blockMeshInstance = pyBlockMesh(fvCFD)
    # create argc and argv in the C style to be passed to generateMesh
    
    print("args: ", args)

    blockMeshInstance.runBlockMesh(args)

def runPatchAverage(project_dir, dictionaries, args):

    fvCFD = fvCFDWrapper(dictionaries)

    patchAverageInstance = pyPatchAverage(fvCFD)

    # Find and print the file names within the project_dir/0 directory
    fields = find_dictionary_files(os.path.join(project_dir, "0"))
    # Cut off the path from each file name
    for i in range(len(fields)):
        fields[i] = os.path.basename(fields[i])
    print(fields)

    field = input("Enter the field to be averaged: ")
    
    print(dictionaries[field]["boundaryField"].keys())

    patch = input("Enter the patch to be averaged: ")

    args.append(field)
    args.append(patch)

    patchAverageInstance.runPatchAverage(args)

