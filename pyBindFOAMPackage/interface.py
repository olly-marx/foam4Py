"""
pyBindFOAM

This script/module is part of the pyBindFOAM project, which provides a Python
interface to OpenFOAM C++. It uses the pybind11 library to generate
bindings to the OpenFOAM C++ API.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    This script is the primary user interface to the pyBindFOAM project. It
    provides a command line interface to the various functions and classes
    provided by the pyBindFOAM library.

Usage:
    

Dependencies:
    - Python 3.5+
    - pybind11
    - foam-extend 5.0

License:


For more information and updates, visit:


"""
# ------------------------------------------------------------------------------
# Import the required modules
from pyBindFOAMPackage import interfaceUtils as iu

# Define the main function
def runInterface():
    # Start by greeting the user and printing something that makes it clear
    # that we are in the pyBindFOAM interface
    greeting = """
    **********************************************************
    *                                                        *
    *                  Welcome to pyBindFOAM!                *
    *                                                        *
    **********************************************************

    pyBindFOAM is a Python interface to the FOAM (OpenFOAM) C++
    library, enabling you to harness the power of OpenFOAM
    capabilities within a Python environment.

    Key Features:
    - Seamless integration of FOAM functionalities in Python scripts.
    - Access to FOAM classes, solvers, utilities, and more.
    - Combine the flexibility of Python with the robustness of FOAM.

    Getting Started:
    1. Import OpenFOAM project directory.
    2. Write "help" to see a list of available commands.
    """
    print(greeting)
    # Now the dictionaries are ready to be used. We will now enter a loop
    # where the user can enter commands to interact with the dictionaries.
    project_dir, dictionaries = iu.import_project()
    iu.print_commands()

    while True:
        # Command input
        user_input = input("\n>>> ")

        if user_input.lower().strip() == "view" or str(user_input.strip()) ==\
                "1" or user_input.lower().strip() == "v":
            # View the contents of a specific dictionary
            iu.view_dictionary(dictionaries)

        elif user_input.lower().strip() == "edit" or str(user_input.strip()) ==\
                "2" or user_input.lower().strip() == "e":
            # Edit the contents of a specific dictionary
            dictionaries = iu.edit_dictionary(project_dir, dictionaries)

        elif user_input.lower().strip() == "help" or str(user_input.strip()) ==\
                "3" or user_input.lower().strip() == "h":
            # Show available commands
            iu.print_commands()

        elif user_input.lower().strip() == "mesh" or str(user_input.strip()) ==\
                "4" or user_input.lower().strip() == "m":
            # Mesh the domain
            iu.mesh_domain(project_dir, dictionaries)            

        elif user_input.lower().strip() == "solve" or str(user_input.strip()) ==\
                "5" or user_input.lower().strip() == "s":
                    print("Solving the case...")
                    print("Done! This isn't implemented yet, but it will be soon! :)")

        elif user_input.lower().strip() == "quit" or str(user_input.strip()) ==\
                "0" or user_input.lower().strip() == "q":
            # Quit the interface
            print("Exiting pyBindFOAM interface. Goodbye!")
            break

        else:
            # Try to interpret the input as a command or an expression
            try:
                exec(user_input)
            except Exception as e:
                print(f"Error: Unknown command '{user_input}'. Type 'help' for available commands.")

