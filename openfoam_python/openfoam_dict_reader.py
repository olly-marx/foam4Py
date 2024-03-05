"""
OpenFOAM Dictionary Reader

A script that contains a function to read an OpenFOAM dictionary file.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    This script contains a function that reads an OpenFOAM dictionary file and returns a nested dictionary
    representation of the file. The function is used by the pyBindFOAM interface to import the dictionaries
    from a given project directory.

Usage: 
    The read_openfoam_dictionary function is used to read an OpenFOAM dictionary file.

Dependencies:
    - Python 3.5+
    - pybind11
    - foam-extend 5.0

License:

For more information and updates, visit:

"""

import json

__all__ = ["read_openfoam_dictionary"]

def read_openfoam_dictionary(file_path):
    """
    Read an OpenFOAM dictionary file and return a nested dictionary representation.

    Args:
        file_path (str): The path to the OpenFOAM dictionary file.

    Returns:
        dict: A nested dictionary representing the contents of the OpenFOAM dictionary file.
    """
    def process_value(lines_iter, line_number):
        # Function to process the value part of a key-value pair
        line = lines_iter[line_number]
        line_number += 1
        if line == "{":
            value, line_number = process_block(lines_iter, line_number)
        elif line == "(":
            value, line_number = process_array(lines_iter, line_number)
        else:
            raise Exception("Invalid dictionary, expected a block or array")

        return value, line_number

    def process_block(lines_iter, line_number):
        # Function to process a block within the dictionary
        result_dict = {}

        while line_number < len(lines_iter):
            line = lines_iter[line_number]
            line_number += 1
            if line == "}":
                break
            elif line.endswith(";"):
                key, value = process_line(line)
                result_dict[key] = value

            elif len(line.split()) == 1:
                key = line.strip()
                value, line_number = process_value(lines_iter, line_number)
                result_dict[key] = value
        return result_dict, line_number


    def process_array(lines_iter, line_number):
        # Function to process an array within the dictionary
        result_list = []
        while line_number < len(lines_iter):
            line = lines_iter[line_number]
            line_number += 1
            if line.startswith(")"):
                break
            elif line.startswith("("):
                result_list.append(process_inline_array(line))
            elif len(line.split()) == 1:
                key = line.strip()
                value, line_number = process_value(lines_iter, line_number)
                if isinstance(value, dict):
                    value = {key: value}
                result_list.append(value)
            elif line.endswith(";"):
                key, value = map(str.strip, line.rstrip(';').split(None, 1))
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                result_list.append(value)
            elif line.startswith("hex"):
                result_list.append(line)
            else:
                result_list += line.split()
        return result_list, line_number

    def process_line(line):
        # Function to process a single line within the dictionary
        key, value = map(str.strip, line.rstrip(';').split(None, 1))

        if value.startswith("["):
            value = process_inline_array(value)

        else:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    if value == "yes":
                        value = True
                    elif value == "no":
                        value = False
                    else:
                        pass
        return key, value

    def process_inline_array(line):
        # Function to process an inline array within the dictionary
        result_list = []
        line_list = line.split()
        for item in line_list:
            item = item.strip("()[]")
            try:
                item = int(item)
            except ValueError:
                try:
                    item = float(item)
                except ValueError:
                    pass
            result_list.append(item)
        return result_list

#******************************************************************************
#                                MAIN BLOCK
#******************************************************************************

    result_dict = {}

    print(f"Reading file '{file_path}'")
    line_number = 0
    line = ""

    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            lines = [line.strip() for line in lines]

            while line_number < len(lines):
                line = lines[line_number].strip()
                line_number += 1

                if line.strip() == "":
                    continue
                elif line.startswith("/"):
                    continue
                elif line.startswith("\\"):
                    continue
                elif line.endswith(";"):
                    key, value = map(str.strip, line.rstrip(';').split(None, 1))
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    result_dict[key] = value
                elif len(line.split()) == 1:
                    if line.isdigit():
                        result_array = []
                        array_len = int(line)

                        result_array, line_number = process_array(lines, line_number)

                        result_dict[str(array_len)] = result_array

                    else:
                        key = line.strip()
                        value, line_number = process_value(lines, line_number)
                        if isinstance(result_dict, list):
                            result_dict.append({key: value})
                        else:
                            result_dict[key] = value

    except Exception as e:
        print(f"Error parsing file '{file_path}' at line {line_number}: {str(e)}")
        print(f"Line: {line}")

    return result_dict

