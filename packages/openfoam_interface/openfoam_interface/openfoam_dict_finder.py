"""
OpenFOAM Dictionary Finder

A script that contains a function to find all the Foam dictionary files in a given directory.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    This script contains a function that finds all the Foam dictionary files in a given directory. The function
    is used by the OpenFOAM interface to import the dictionaries from a given project directory.

Usage: 
    The find_dictionary_files function is used to find all the Foam dictionary files in a given directory.

Dependencies:
    - Python 3.5+
    - pybind11
    - foam-extend 5.0

License:

For more information and updates, visit:

"""

import os
import linecache

__all__ = ["find_dictionary_files"]

def is_nonuniform(file_path):
    """
    Check if the given file contains the "nonuniform" keyword.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file contains "nonuniform", False otherwise.
    """
    try:
        # Read a few lines from the file to check for the "nonuniform" keyword
        lines_to_read = 20
        lines = [linecache.getline(file_path, i) for i in range(1, lines_to_read + 1)]

        # Check if any of the lines contain the "nonuniform" keyword
        return any("nonuniform" in line for line in lines)
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False

def is_highmemory(file_path):
    """
    Check if the given file is a high memory file.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is high memory, False otherwise.
    """
    try:
        # If the file is called points, faces, owner, or neighbour, it is high memory
        return any(file_name in file_path for file_name in ["points", "faces", "owner", "neighbour", "profilingInfo", "time"])
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False

def find_dictionary_files(directory):
    """
    Find all the Foam dictionary files in the given directory.

    Args:
        directory (str): The directory to search for dictionary files.

    Returns:
        list: A list of paths to the dictionary files.
    """
    dictionary_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a dictionary and if it is nonuniform any file
            # with a "." in it is not a dictionary
            valid_file = (not is_nonuniform(os.path.join(root, file))\
                    and not is_highmemory(os.path.join(root, file)))
            if not "." in file and valid_file:
                file_path = os.path.join(root, file)
                dictionary_files.append(file_path)
    return dictionary_files

