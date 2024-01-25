"""
This module contains functions for reading and writing OpenFOAM dictionaries.
"""
#Import required modules
import json

def read_openfoam_dictionary(file_path):
    """
    Reads an OpenFOAM dictionary file and returns a dictionary of the contents.
    """
    def process_value(lines_iter, line_number):
        print(line_number)
#        print(lines_iter[line_number])
        if lines_iter[line_number]=="{":
            print("entering block")
            value, line_number = process_block(lines_iter,line_number)
        elif lines_iter[line_number]=="(":
            print("entering array")
            value, line_number = process_array(lines_iter,line_number)
        else:
            raise Exception("Invalid dictionary, expected a block or array")

        return value, line_number

    # a function to process a block of lines, i.e. a dictionary
    def process_block(lines_iter, line_number):
        result_dict = {}
        line_number += 1
        print("in block"+str(line_number))
#        print(lines_iter[line_number:])
        # Iterate over the lines in the block
        while line_number < len(lines_iter):
            line = lines_iter[line_number]
            if line == "}":
                line_number += 1
                break  # End of the block
            elif line.endswith(";"):
                key, value = map(str.strip, line.rstrip(';').split(None, 1))
                result_dict[key] = value
                print("added to dict"+key+value)
                line_number += 1
            # The start of a nested block will just be a key
            elif len(line.split()) == 1:
                line_number += 1
                key = line.strip()
                print(key)
                value,new_line_number = process_value(lines,line_number)
                result_dict[key] = value
                line_number = new_line_number
                print("end of process_value nested"+str(line_number))
        print("printing at the end of process_block")
        return result_dict, line_number

    def process_array(lines_iter, line_number):
        result_list = []
        line_number += 1
        print("in array"+str(line_number))
        print(lines_iter[line_number:])
        while line_number < len(lines_iter):
            line = lines_iter[line_number]
            if line==");":
                print("closed the list")
                line_number += 1
                break  # End of the array
            elif line.startswith("("):
                result_list.append(process_inline_array(line))
                line_number += 1
            elif len(line.split()) == 1:
                line_number += 1
                key = line.strip()
                print(key)
                value,new_line_number = process_value(lines,line_number)
                # If the value is a dictionary, we create a single item
                # dictionary with the key as the key and the value as the value
                if(isinstance(value, dict)):
                    value = {key: value}
                result_list.append(value)
                line_number = new_line_number
                print("end of process_value nested"+str(line_number))
            elif line.endswith(";"):
                key, value = map(str.strip, line.rstrip(';').split(None, 1))
                result_list.append(value)
                print("added to dict"+key+value)
                line_number += 1
            else:
                result_list += line.split()
            print(result_list)
        print("printing at the end of process_array")
        return result_list, line_number

    def process_inline_array(line):
        result_list = []
        # Remove the leading and trailing parentheses
        line = line.strip("()")
        # Split the line into a list of strings
        line_list = line.split()
        # Iterate over the strings in the list
        for item in line_list:
            # The string is a value
            result_list.append(item)
        return result_list

    result_dict = {}
    is_comment_block = False

    try:
        with open(file_path, 'r') as file:
            # Split the file into a list of lines without newlines
            lines = file.read().splitlines()
            # Strip whitespace from the start and end of each line
            lines = [line.strip() for line in lines]

            line_number = 14
#            print(len(lines))
            while line_number < len(lines):
                line_number += 1
#                print(str(line_number) + " " + lines[line_number])
                line = lines[line_number]
                # Check for the end of the comment block
                if line.startswith("// *"):
                    is_comment_block = False
                    continue

                # Check for the start of the comment block
                if line.startswith("/*"):
                    is_comment_block = True
                    continue

                if not line.strip():
                    continue
                
                # If not in a comment block, process the line
                if not is_comment_block and line.strip():
                    # Check for the start of a block, will be of the form
                    # key value;
                    # or if it is just a key, it will be of the form
                    # key then the next line will be
                    # { or (
                    if line.endswith(";"):
                        key, value = map(str.strip, line.rstrip(';').split(None, 1))
                        result_dict[key] = value
                        print("added to dict"+key+value)
                    # The start of a block will just be a key
                    elif len(line.split()) == 1:
                        line_number += 1
                        key = line.strip()
                        print(key)
                        value,new_line_number = process_value(lines,line_number)
                        result_dict[key] = value
                        line_number = new_line_number
                        print("returned from process_value"+str(line_number))
                print(line_number)
                print(key+" : "+str(value))
                result_dict[key] = value
    except Exception as e:
        print(f"Error parsing file '{file_path}' at line {line_number}: {str(e)}")


    return json.dumps(result_dict)
