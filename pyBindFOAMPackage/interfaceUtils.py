#!/usr/bin/env python3

import os
import sys
import subprocess
from pyBindFOAMPackage import importFoamDict as ifd
from pyBindFOAMPackage import findFoamDicts as ffd
import json
import datetime as dt

# Function to print available commands
def print_commands():
    commands = """
    Available Commands:
    1. view (v) - View the contents of a specific dictionary.
    2. edit (e) - Edit the contents of a specific dictionary.
    3. help (h) - Show available commands.
    4. mesh (m) - Run the meshing utility blockMesh.
    5. solve (s) - Run the solver specified in the controlDict file.
    6. postprocess (p) - Postprocess the case.
    0. quit (q) - Exit the pyBindFOAM interface.

    You can also use normal Python commands, e.g. print(dictionaries.keys())
    """
    print(commands)

def print_options(section):
    options = ""
    if section == "mesh":
        options = """
        **********************************************************
        *                                                        *
        *  Meshing Options:                                      *
        *                                                        *
        *  1. Generate the mesh (blockMesh) [bm]                 *
        *  0. Return to the main menu (back) [b]                 *
        *                                                        *
        **********************************************************
        """
    elif section == "postprocess":
        options = """
        **********************************************************
        *                                                        *
        *  Postprocessing Options:                               *
        *                                                        *
        *  1. Calculate the patch averages (patchAverages) [pa]  *
        *  0. Return to the main menu (back) [b]                 *
        *                                                        *
        **********************************************************
        """
    print(options)

# Function to import an OpenFOAM project directory
def import_project():
    while True:
        # The first prompt will be to import an OpenFOAM project directory.
        project_dir = input("Enter the path to the OpenFOAM project directory: ")
        # Check if the directory exists
        if not os.path.isdir(project_dir):
            raise ValueError("The specified directory does not exist.")
            continue
        if not os.path.isfile(os.path.join(project_dir, "system/controlDict")):
            raise ValueError("The specified directory is not a valid OpenFOAM"+\
                    "project. \n no controlDict file found in the system"+\
                    "directory.")
            continue
        if not os.path.isdir(os.path.join(project_dir, "constant")):
            raise ValueError("The specified directory is not a valid OpenFOAM"+\
                    "project. \n no constant directory found.")
        if not os.path.isdir(os.path.join(project_dir, "0")):
            raise ValueError("The specified directory is not a valid OpenFOAM"+\
                    "project. \n no 0 directory found.")
            continue

        break

    dictionary_files = ffd.find_dictionary_files(project_dir)
    print("Found the following dictionary files:")
    for file_path in dictionary_files:
        print(file_path)
    dictionaries = {}

    for file_path in dictionary_files:
        #print(f"Processing: {file_path}")

        # We will store the dictionaries in a dictionary of dictionaries.
        # The key will be the name of the dictionary file, and the value
        # will be the dictionary itself.
        key = os.path.basename(file_path)
        dictionaries[key] = ifd.read_openfoam_dictionary(file_path)
        print(f"Dictionary {key} successfully imported.")

    # For each dictionary, we will recursively print the contents of the
    # dictionary to the screen.
    #for key in dictionaries.keys():
    #    print(f"Dictionary: {key}")
    #    print("------------------------------------------------------------")
    #    ifd.print_nested_dict(dictionaries[key])
    #    print("------------------------------------------------------------")

    print("Checking for history of dictionary changes...")
    # Look in this directory for the history.json file. If it exists, then
    # we will load it and use it to update the dictionaries.
    history_file = os.path.join(project_dir, "_history.json")
    # We need to load it as a json
    if os.path.isfile(history_file):
        f = open(history_file)
        history = json.load(f)
        print("History found. Importing changes...")
    else:
        # create a history file and initialize it with an empty dictionary
        history = {}
        f = open(history_file, "w")
        json.dump(history, f)

    # Now looping through the history, we will update the dictionaries
    # If the history dictionary has no keys, then this loop will not run.
    if len(history.keys()) > 0:
        for key in history.keys():
            history_command = history[key]['edit']
            dictionaries = edit_dictionary_string(dictionaries, history_command)

    return project_dir, dictionaries


# Function to view the contents of a specific dictionary
def view_dictionary(dictionaries):
    print("Available dictionaries:")
    for key in dictionaries.keys():
        print(f"- {key}")

    dictionary_name = input("Enter the name of the dictionary to view: ")
    if dictionary_name in dictionaries:
        print(f"\nDictionary: {dictionary_name}")
        print("------------------------------------------------------------")
        ifd.print_nested_dict(dictionaries[dictionary_name])
        print("------------------------------------------------------------")
    else:
        print(f"Error: Dictionary '{dictionary_name}' not found.")
# ------------------------------------------------------------------------------

def edit_instructions():
    instructions = [
    "1. For a simple key-value pair:",
    "   key = value",
    "   Note: the value can be a string, integer, float, or boolean."
    "   e.g. deltat = 0.001 OR writeControl = \"timeStep\"",
    "",
    "2. For a value in a nested dictionary:",
    "   nested_dictionary_name.key = value",
    "   e.g. turbulenceProperties.RAS.model = \"kEpsilon\"",
    "",
    "3. For a list of values:",
    "   key = [value1, value2, value3]",
    "   e.g. vertices = [0.0, 0.0, 0.0]",
    "",
    "4. For a list of values in a nested dictionary:",
    "   nested_dictionary_name.key = [value1, value2, value3]",
    "   e.g. boundaryField.inlet.value = [0.0, 0.0, 0.0]",
    "",
    "5. For an entry in a list:",
    "   key[index] = value",
    "   e.g. vertices[0] = 0.0",
    "",
    "To edit the dictionary:",
    "1. Enter a 'key = value' pair and hit enter to add it to the dictionary.",
    "2. To exit edit mode, enter a period (.) and hit enter.",
    "",
    "Formatting is important. Follow the provided examples."
    ]

    for instruction in instructions:
        print(instruction)


# Function to edit the contents of a specific dictionary
def edit_dictionary(project_dir, dictionaries):

    history_file = os.path.join(project_dir, "_history.json")
    if os.path.isfile(history_file):
        f = open(history_file)
        history = json.load(f)

    print("Available dictionaries:")
    for key in dictionaries.keys():
        print(f"- {key}")

    dictionary_name = input("Enter the name of the dictionary to edit: ")
    if dictionary_name in dictionaries:
        print(f"\nDictionary: {dictionary_name}")
        print("------------------------------------------------------------")
        ifd.print_nested_dict(dictionaries[dictionary_name])
        print("------------------------------------------------------------")

        # Now we will ask the user to enter a key = value pair and then hit enter
        # to add it to the dictionary. We will continue to do this until the user
        # enters a period (.) and then hits enter.
        print("Enter your edits below. Enter \"help\" for edit instructions.\n"+\
                "Enter a period (.) to exit edit mode.")

        while True:
            # Get the user input
            user_input = input(">> ")
            # Check if the user wants to exit edit mode
            if user_input == ".":
                print("Exiting edit mode...")
                break
            # Check if the user wants to see the edit instructions
            if user_input == "help":
                edit_instructions()
                continue
            # Split the user input into key and value. We need a way to find
            # nested dictionaries. We will use the = sign to split the string.
            try:
                user_input = f"{dictionary_name}." + user_input
                user_keys, user_value = user_input.split("=")
                user_keys = user_keys.strip().split(".")
                command = "dictionaries"
                for key in user_keys:
                    command += f"[\'{key}\']"
                command += f" = {user_value.strip()}"
                print(command)
                exec(command, globals(), locals())
                print(f"Added: {key} = {user_value}")
            except Exception as e:
                print(f"Error: {e}. Invalid edit. Try again.")
                continue

            # Get the current datetime from the datetime module
            now = dt.datetime.now()
            # Format the datetime
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            # Get the user name
            user = os.getlogin()
            # Create the history entry
            history_entry = {dt_string: {"editedby": user, "edit": command}}
            # Now add the history entry to the history dictionary
            history.update(history_entry)

            # Now we will write the history dictionary to the history file
            with open(history_file, "w") as f:
                json.dump(history, f, indent=4)
    else:
        print(f"Error: Dictionary '{dictionary_name}' not found.")

    return dictionaries

# Overloaded function to edit based on a string command
def edit_dictionary_string(dictionaries, history_command):
    try:
        exec(history_command, globals(), locals())
    except Exception as e:
        print(f"Error: {e}. Invalid edit. Try again.")

    return dictionaries
