import sys
import os

pybind11_folder = '../src/patchAverage/Make/linux64GccDPInt32Opt'

sys.path.append(os.path.abspath(pybind11_folder))

import pyBindPatchAverage as patchAverage

def main():
    patchAverage.calculatePatchAverage()

if __name__ == "__main__":
    main()

