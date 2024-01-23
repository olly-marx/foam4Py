import sys
import os

import pyBindFOAMPackage

def main():
    libpyBindFOAM.patchAverage.calculateAverages()

    # print the methods that are available in the module
    print(dir(patchAverage))

if __name__ == "__main__":
    main()

