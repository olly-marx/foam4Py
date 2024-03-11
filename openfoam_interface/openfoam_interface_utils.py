"""
interfaceUtils.py

A script that contains utility functions for the OpenmFOAM interface.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    This script contains utility functions for the OpenFOAM interface. The functions
    are used to print the greeting, print available commands, import an OpenFOAM project
    directory, view the contents of a specific dictionary, edit the contents of a specific
    dictionary, and run the meshing and postprocessing utilities.

Usage: 
    The functions in this script are called by the OpenFOAM interface.

Dependencies:
    - Python 3.5+
    - pybind11
    - foam-extend 5.0

License:

For more information and updates, visit:

"""

import os
import sys
from .openfoam_dict_reader import *
from .openfoam_dict_finder import *
from .output_interface import *
from .dictionary_editor import *
from .state import *

__all__ = ["import_project", "list", "view", "edit_dict_selected", "solve", "autocompletes"]

def import_project():
    """
    Prompt the user to enter the path to the OpenFOAM project directory and import
    the dictionaries found within it.

    Returns:
        tuple: A tuple containing the project directory path and a dictionary of
        imported dictionaries.
    """
    while True:
        
        project_dir = input("Enter the path to the OpenFOAM project directory:\n>>> ").strip()

        if project_dir == "q":
            print("Exiting pyBindFOAM interface. Goodbye!")
            sys.exit()

        if not os.path.isdir(project_dir):
            print("The specified directory does not exist.\n If you wish to exit, enter 'q'.")
            continue
            
        if not os.path.isfile(os.path.join(project_dir, "system/controlDict")):
            print("The specified directory is not a valid OpenFOAM project.\nNo controlDict file found in the system directory.\n If you wish to exit, enter 'q'.")
            continue

        if not os.path.isdir(os.path.join(project_dir, "constant")):
            print("The specified directory is not a valid OpenFOAM project.\nNo constant directory found.\n If you wish to exit, enter 'q'.")
            continue

        if not os.path.isdir(os.path.join(project_dir, "0")):
            print("The specified directory is not a valid OpenFOAM project.\nNo 0 directory found.\n If you wish to exit, enter 'q'.")
            continue

        break

    dictionary_files = find_dictionary_files(project_dir)
    print("Found the following dictionary files:")
    for file_path in dictionary_files:
        print(file_path)
    dictionaries = {}

    for file_path in dictionary_files:
        # Set the dictionary name as the key keeping the parent directory
        key = file_path.split("/")[-2] + "." + file_path.split("/")[-1]
        dictionaries[key] = read_openfoam_dictionary(file_path)
        print(f"Dictionary {key} successfully imported.")
            
    editor = DictionaryEditor(project_dir)
    editor.import_history(dictionaries)

    return project_dir, dictionaries

def list(state):
    """
    Print a list of available dictionaries.

    Args:
        state (InterfaceState): The current state of the interface.
    """
    print_list(state)

def view(state):
    """
    View the contents of a specific dictionary.

    Args:
        state (InterfaceState): The current state of the interface.

    Returns:
        InterfaceState: The updated state of the interface.
    """
    if state.state == STATE.VIEW:
        list(state)

        dictionary_name = state.viewing_dictionary

        if dictionary_name in state.dictionaries:
            print(f"\nDictionary: {dictionary_name}")
            print("------------------------------------------------------------")
            print_dict(state.dictionaries, dictionary_name)
            print("------------------------------------------------------------")

        else:
            print(f"Error: Dictionary '{dictionary_name}' not found.")

    elif state.state == STATE.SELECTING_DICT:
        list(state)

    elif state.state == STATE.EDITING_DICT:

        dictionary_name = state.editing_dictionary
        print(f"\nDictionary: {dictionary_name}")
        print("------------------------------------------------------------")
        print_dict(state, dictionary_name)
        print("------------------------------------------------------------")

    else:
        print("View command only available from home. Enter 'home' or '.' to return to home.\n")

    return state

def edit_dict_selected(state):
    """
    Edit the contents of a selected dictionary.

    Args:
        state (InterfaceState): The current state of the interface.

    Returns:
        tuple: A tuple containing an error flag and the updated state of the interface.
    """
    dictionary_name = state.editing_dictionary
    error = 0

    if dictionary_name in state.dictionaries:

        print_help(state)

        state.editing_dictionary = dictionary_name

        print(f"\nDictionary: {dictionary_name}")
        print("------------------------------------------------------------")
        print_dict(state.dictionaries, dictionary_name)
        print("------------------------------------------------------------")

        # Update the autocomplete dictionary
        state.locals.clear()
        autocomplete = autocompletes(state)
        state.locals.update(autocomplete)

        state.editor.edit(state.dictionaries[dictionary_name])

    else:
        print(f"Error: Dictionary '{dictionary_name}' not found.")
        error = 1

    return error, state

def solve(state):
    """
    Perform solving operation.

    Args:
        state (InterfaceState): The current state of the interface.
    """
    controlDict = state.dictionaries["system/controlDict"]

    solver = controlDict["application"]

    try:
        solver = "run" + solver[0].upper() + solver[1:]
        eval(f"foam.{solver}(state.project_dir, state.dictionaries, state.args)")

    except Exception as e:
        print(f"Error: {e}. Solver '{solver}' not found. Please check controlDict.")

def autocompletes(state):
    """
    Generate autocomplete options based on the current state of the interface.

    Args:
        state (InterfaceState): The current state of the interface.

    Returns:
        dict: A dictionary of autocomplete options.
    """
    autocomplete = {}
    for command in state.PERMANENT_COMMANDS:
        autocomplete[command] = state.PERMANENT_COMMANDS[command]

    if state.state == STATE.HOME:
        for command in state.HOME_COMMANDS:
            autocomplete[command] = state.HOME_COMMANDS[command]

    elif state.state == STATE.VIEW:
        for command in state.DICT_AUTOCOMPLETE:
            autocomplete[command] = state.DICT_AUTOCOMPLETE[command]

    elif state.state == STATE.SELECTING_DICT:
        for command in state.DICT_AUTOCOMPLETE:
            autocomplete[command] = state.DICT_AUTOCOMPLETE[command]

    elif state.state == STATE.MESH:
        for command in state.MESH_COMMANDS:
            autocomplete[command] = state.MESH_COMMANDS[command]

    elif state.state == STATE.MESH:
        for command in state.POST_COMMANDS:
            autocomplete[command] = state.POST_COMMANDS[command]

    elif state.state == STATE.EDITING_DICT:
        dictionary_name = state.editing_dictionary
        dictionary = state.dictionaries[dictionary_name]
        EDITING_COMMANDS = state.populate_EDITING_COMMANDS(dictionary, [], {})
        for command in EDITING_COMMANDS:
            autocomplete[command] = EDITING_COMMANDS[command]
    
    return autocomplete

