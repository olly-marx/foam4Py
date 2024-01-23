import sys
import os

from pyBindFOAMPackage import patchAverage

def main():
    patchAverageInstance = patchAverage("U","movingWall")
    patchAverageInstance.calculateAverage()

if __name__ == "__main__":
    main()

