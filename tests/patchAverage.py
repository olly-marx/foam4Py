import sys
import os

lib_folder = "../src/pyBindFOAM"

sys.path.append(os.path.abspath(lib_folder))

import libpyBindFOAM

def main():
    libpyBindFOAM.patchAverage.calculateAverages()

    # print the methods that are available in the module
    print(dir(patchAverage))

if __name__ == "__main__":
    main()

