import os
import linecache

def is_nonuniform(file_path):
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
    try:
        # If the file is called points, faces, owner, or neighbour, it is high memory
        return any(file_name in file_path for file_name in ["points", "faces", "owner", "neighbour"])
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return False

def find_dictionary_files(directory):
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

