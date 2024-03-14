"""
This module contains functions for printing output messages and help
information to the console.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    This module contains functions for printing output messages and help
    information to the console. It is used by the OpenFOAM interface to
    to display information to the user.

Usage:
    The functions in this module are used to print output messages and
    help information to the console.
"""

from .state import *

__all__ = ["print_greeting", "print_help", "print_list", "print_dict"]

def print_greeting():
    """
    Print a welcome message with information about pyBindFOAM.
    """
    greeting = """
    **********************************************************
    *                                                        *
    *                  Welcome to OpenFOAM!                *
    *                                                        *
    **********************************************************

    This is an OpenFOAM interface that allows you to interact with OpenFOAM
    through the foam4Py library.

    Key Features:
    - Seamless integration of FOAM functionalities in Python script
    - Access to FOAM classes, solvers, utilities, and more.
    - Combine the flexibility of Python with the robustness of FOAM.

    Getting Started:
    1. Import OpenFOAM project directory.
    2. View and edit the project dictionarie
    3. Run the meshing and solving utilitie
    4. Execute post-processing utilitie
    """
    print(greeting)

def print_help(state):
    """
    Print help message based on the current state of the interface.

    Args:
        state (InterfaceState): The current state of the interface.
    """
    commands = ""
    if state.state == STATE.HOME:
        commands = """
        Permanent Commands:
        [h]elp    - Print a list of available commands or action
        [q]uit    - Exit the pyBindFOAM interface.
        [.][home] - Return to home.

        Home Commands:
        [l]ist  - List the current OpenFOAM project dictionarie
        [v]iew  - View the contents of a specific dictionary.
        [e]dit  - Edit a specific dictionary.
        [m]esh  - Run the meshing utility blockMesh.
        [s]olve - Run the solver specified in the controlDict file.
        [p]ost  - Execute a post-processing utility.
        """
    elif state.state == STATE.MESH:
        commands = """
        Meshing Commands:
        [bl]ockMesh - Run the blockMesh utility.

        [.][home]   - Return to home.
        """
    elif state.state == STATE.POST:
        commands = """
        Post-Processing Commands:
        [pa]tchAverage - Run the patchAverage utility.

        [.][home]      - Return to home.
        """
    elif state.state == STATE.VIEW:
        dicts = state.dictionaries.keys()
        commands = "Available dictionaries: " + str(dicts) + "\n"

    elif state.state == STATE.SELECTING_DICT:
        commands = """
        Select a dictionary to edit ([l]ist to see available dictionaries):
        """

    elif state.state == STATE.EDITING_DICT:
        commands = """
        Dictionary Adding/Editing Commands:
        [sa]ve   - Save and go back.
        [ca]ncel - Cancel and go back.
        [.]      - Save and return to home.

        1. For a simple key-value pair:
           key = value
           Note: the value can be a string, integer, float, or boolean
           e.g. deltat = 0.001 OR writeControl = \"timeStep\"
        
        2. For a value in a nested dictionary:
           nested_dictionary_name.key = value
           e.g. turbulencePropertieRAS.model = \"kEpsilon\"
        
        3. For a list of values:
           key = [value1, value2, value3]
           e.g. vertices = [0.0, 0.0, 0.0]
        
        4. For a list of values in a nested dictionary:
           nested_dictionary_name.key = [value1, value2, value3]
           e.g. boundaryField.inlet.value = [0.0, 0.0, 0.0]
        
        5. For an entry in a list:
           key[index] = value
           e.g. vertices[0] = 0.0
        
        To edit the dictionary:
        1. Enter a 'key = value' pair and hit enter to add it to the dictionary.
        2. To exit edit mode, enter a period (.) and hit enter.
        
        Formatting is important. Follow the provided examples
        and the OpenFOAM dictionary format.
        """

    print(commands)
    print(state.get_state_string())

def print_list(state):
    """
    Print a list of available dictionaries or command

    Args:
        state (InterfaceState): The current state of the interface.
    """
    list_output = ""
    if state.state == STATE.HOME:
        list_output += "\nOpenFOAM project dictionaries:\n"
        for key in state.dictionaries.keys():
            list_output += f"- {key}\n"

    elif state.state == STATE.VIEW:
        list_output +="\nAvailable dictionaries to view:\n"
        for key in state.dictionaries.keys():
            list_output += f"- {key}\n"

    elif state.state == STATE.SELECTING_DICT:
        list_output += "\nAvailable dictionaries to edit:\n"
        for key in state.dictionaries.keys():
            list_output += f"- {key}\n"

    elif state.state == STATE.EDITING_DICT:
        print_dict(state.dictionaries, state.selected_dict)

    elif state.state == STATE.MESH:
        print_help(state)

    elif state.state == STATE.POST:
        print_help(state)

    print(list_output)
    print(state.get_state_string())

def print_dict(stateDicts, dictionary_name=None, indent=0):
    """
    Print the contents of a dictionary.

    Args:
        stateDicts (dict): The dictionary or nested dictionary to print.
        dictionary_name (str): The name of the dictionary.
        indent (int): The indentation level.
    """
    if dictionary_name is None:
        d = stateDicts
    else:
        d = stateDicts[dictionary_name]

    for key, value in d.items():
        if isinstance(value, dict):
            print(f"{' ' * indent}{key}: {{")
            print_dict(value, None, indent + 2)
            print(f"{' ' * indent}}}")
        elif isinstance(value, list):
            print(f"{' ' * indent}{key}: [")
            for item in value:
                if isinstance(item, dict):
                    print(f"{' ' * (indent + 2)}{{")
                    print_dict(item, None, indent + 4)
                    print(f"{' ' * (indent + 2)}}},")
                else:
                    print(f"{' ' * (indent + 2)}{item},")
            print(f"{' ' * indent}]")
        else:
            print(f"{' ' * indent}{key}: {value},")

