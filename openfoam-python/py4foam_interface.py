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
    Instantiate the InterfaceState class and call the run_interface() method.

Dependencies:
    - Python 3.5+
    - pybind11
    - foam-extend 5.0

License:

For more information and updates, visit:

"""

# ------------------------------------------------------------------------------
# Import the required modules
import sys
import code
import readline
from .py4foam_interface_utils import *
from .run_foam_executables import *
from .output_interface import *
from .dictionary_editor import *
from .state import *

#*******************************************************************************
#                                INTERFACE s.STATE
#*******************************************************************************

class InterfaceState(code.InteractiveInterpreter):
    """
    InterfaceState class provides a command line interface to the pyBindFOAM library.

    Attributes:
        project_dir (str): Path to the project directory.
        dictionaries (dict): Dictionaries available for editing.
        args (list): Command line arguments.
        state (s.STATE): Current state of the interface.
        state_stack (list): Stack to keep track of state transitions.
        editor (dictionaryEditor.DictionaryEditor): Editor instance.
        editing_dictionary (str): Name of the currently editing dictionary.
        PERMANENT_COMMANDS (dict): Permanent commands available in all states.
        HOME_COMMANDS (dict): Commands available in HOME state.
        MESH_COMMANDS (dict): Commands available in MESH state.
        POST_COMMANDS (dict): Commands available in POST state.
        DICT_AUTOCOMPLETE (dict): Dictionary for autocompletion.
        EDITING_COMMANDS (dict): Commands available in EDITING_DICT state.
    """

    def __init__(self, local=None):
        if local is None:
            local = {}
        super().__init__(local)

        # Initialization
        out.print_greeting()
        self.project_dir, self.dictionaries = iu.import_project()
        self.args = sys.argv
        self.state = s.STATE.HOME
        self.state_stack = [self.state]
        self.editor = DictionaryEditor(self.project_dir)
        self.editing_dictionary = None
        out.print_help(self)

        # Define command dictionaries
        self.PERMANENT_COMMANDS = {
            'home': self.home,
            '.': self.home,
            'quit': self.quit,
            'q': self.quit,
            'help': self.help,
            'h': self.help,
            'list': self.list_,
            'l': self.list_,
            'back': self.go_back,
            'b': self.go_back,
        }

        self.HOME_COMMANDS = {
            'view': self.view_mode,
            'v': self.view_mode,
            'edit': self.selecting_mode,
            'e': self.selecting_mode,
            'mesh': self.meshing_mode,
            'm': self.meshing_mode,
            'solve': self.solve,
            's': self.solve,
            'post': self.postprocessing_mode,
            'p': self.postprocessing_mode,
        }

        self.MESH_COMMANDS = {
            'blockMesh': self.blockMesh,
            'bl': self.blockMesh,
        }

        self.POST_COMMANDS = {
            'patchAverage': self.patchAverage,
            'pa': self.patchAverage,
        }

        self.DICT_AUTOCOMPLETE = {}
        self.EDITING_COMMANDS = {}

        self.populate_DICT_AUTOCOMPLETE()

    def interact(self, banner=None, exitmsg=None):
        """
        Start the interactive interface.
        """
        self.locals = {}
        self.locals.update(iu.autocompletes(self))
        try:
            prefill = ""
            while True:
                try:
                    def hook():
                        readline.insert_text(prefill)
                        readline.redisplay()
                    readline.set_pre_input_hook(hook)
                    user_input = input(">>> ").strip()

                    if not user_input:
                        prefill = ""
                        continue

                    if user_input == ".":
                        user_input = "home()"
                        self.runsource(user_input)
                    elif user_input in self.locals and callable(self.locals[user_input]):
                        user_input += "()"
                        self.runsource(user_input)
                    elif self.state == s.STATE.VIEW:
                        self.view_dict(user_input)
                        continue
                    elif self.state == s.STATE.SELECTING_DICT:
                        self.editing_mode(user_input)
                        continue
                    elif self.state == s.STATE.EDITING_DICT:
                        prefill = self.edit_dict(user_input)
                        continue
                    else:
                        self.runsource(user_input)

                except (KeyboardInterrupt, EOFError):
                    print()
                    break

        finally:
            if exitmsg:
                print(exitmsg)

    def run_interface(self):
        """
        Run the interface.
        """
        self.interact(banner=None, exitmsg="Exiting pyBindFOAM interface. Goodbye!")

    #*******************************************************************************
    #                         MODE CHANGE COMMANDS
    #*******************************************************************************

    def view_mode(self):
        """
        Switch to VIEW mode.
        """
        if self.check_valid_command("view"):
            if self.state == s.STATE.HOME:
                self.change_state(s.STATE.VIEW)
                self.list_()
                print("Enter the name of the dictionary to view (or '.' to return to home):")
            else:
                iu.view(self)
        else:
            print("Error: Command 'view' not available in current state.")

    def selecting_mode(self):
        """
        Switch to SELECTING_DICT mode.
        """
        if self.check_valid_command("edit"):
            self.change_state(s.STATE.SELECTING_DICT)
            self.list_()
            print("Enter the name of the dictionary to edit (or '.' to return to home):")

    def editing_mode(self, user_input):
        """
        Switch to EDITING_DICT mode.
        """
        if user_input in self.dictionaries.keys():
            self.editing_dictionary = user_input
            self.editor.edit(self.dictionaries[user_input])
            self.change_state(s.STATE.EDITING_DICT)
            iu.edit_dict_selected(self)
        else:
            print(f"Error: Dictionary '{user_input}' not found.")

    def meshing_mode(self):
        """
        Switch to MESH mode.
        """
        if self.check_valid_command("mesh"):
            self.change_state(s.STATE.MESH)
            out.print_help(self)

    def postprocessing_mode(self):
        """
        Switch to POST mode.
        """
        if self.check_valid_command("post"):
            self.change_state(s.STATE.POST)
            out.print_help(self)

    def home(self):
        """
        Go back to HOME mode.
        """
        if self.state == s.STATE.EDITING_DICT and self.editor and self.editor.are_you_sure("go home"):
            self.editor.save_edits()
        self.change_state(s.STATE.HOME)

    def go_back(self):
        """
        Go back to previous mode.
        """
        if self.state == s.STATE.EDITING_DICT and self.editor and self.editor.are_you_sure("go back"):
            self.editor.save_edits()
        if len(self.state_stack) > 1:
            previous_state = self.state_stack[-2]
            self.change_state(previous_state)
            self.state_stack.pop()
        else:
            print("In home. Cannot go back.")

    def save(self):
        """
        Save edits and go back to HOME mode.
        """
        if self.editor:
            self.editor.save_edits()
        self.home()

    def cancel(self):
        """
        Cancel edits and go back to HOME mode.
        """
        if self.editor and self.editor.are_you_sure("cancel"):
            self.home()

    #*******************************************************************************
    #                             ACTION COMMANDS
    #*******************************************************************************

    def help(self):
        """
        Display help message.
        """
        out.print_help(self)

    def list_(self):
        """
        List available dictionaries.
        """
        out.print_list(self)

    def view_dict(self, user_input):
        """
        View a dictionary.
        """
        if user_input in self.dictionaries.keys():
            self.viewing_dictionary = user_input
            iu.view(self)
            self.viewing_dictionary = None
            self.home()
        else:
            print(f"Error: Dictionary '{user_input}' not found.")

    def edit_dict(self, user_input):
        """
        Edit a dictionary.
        """
        if user_input in self.locals:
            prefill = f"{self.locals[user_input]}"
            return prefill
        elif user_input.split("=")[0].strip() in self.locals \
        and  user_input.split("=")[1].strip() != "":
            keys = user_input.split("=")[0]
            value = user_input.split("=")[1]
            self.editor.make_temporary_edit(self.editing_dictionary, keys, value)
            return ""

    def solve(self):
        """
        Perform solving operation.
        """
        if self.check_valid_command("solve"):
            iu.solve(self)
            self.home()

    def blockMesh(self):
        """
        Perform block meshing operation.
        """
        if self.check_valid_command("blockMesh"):
            foamExe.runBlockMesh(self.project_dir, self.dictionaries, self.args)
            self.home()

    def patchAverage(self):
        """
        Perform patch averaging operation.
        """
        if self.check_valid_command("patchAverage"):
            foamExe.runPatchAverage(self.project_dir, self.dictionaries, self.args)
            self.home()

    def quit(self):
        """
        Quit the interface.
        """
        if self.state == s.STATE.EDITING_DICT and self.editor != None and self.editor.are_you_sure("quit"):
            sys.exit()
        else:
            sys.exit()

    #*******************************************************************************
    #                                FUNCTIONS
    #*******************************************************************************

    def change_state(self, nextState):
        """
        Change the state of the interface.
        """
        self.state = nextState
        self.state_stack.append(self.state)
        self.locals = {}
        self.locals.update(iu.autocompletes(self))
        print(self.get_state_string())

    def populate_DICT_AUTOCOMPLETE(self):
        """
        Populate dictionary autocomplete.
        """
        for key in self.dictionaries.keys():
            self.DICT_AUTOCOMPLETE[key] = f"{key}"

    def check_valid_command(self, command):
        """
        Check if command is valid in the current state.
        """
        always_commands = ["help", "quit", "home", "list", "back"]
        always_commands += ["h", "q", ".", "l", "b"]
        home_commands = ["view", "edit", "mesh", "solve", "post"]
        home_commands += ["v", "e", "m", "s", "p"]
        mesh_commands = ["blockMesh"]
        mesh_commands += ["bl"]
        post_commands = ["patchAverage"]
        post_commands += ["pa"]
        view_commands = []
        edit_commands = ["view", "v"]
        edit_sub_commands = ["save", "cancel"]
        edit_sub_commands += ["sa", "ca"]

        if command in always_commands:
            return True
        elif command in home_commands and self.state == s.STATE.HOME:
            return True
        elif command in mesh_commands and self.state == s.STATE.MESH:
            return True
        elif command in post_commands and self.state == s.STATE.POST:
            return True
        elif command in view_commands and self.state == s.STATE.VIEW:
            return True
        elif command in edit_commands and self.state == s.STATE.SELECTING_DICT:
            return True
        elif command in edit_sub_commands and self.state == s.STATE.EDITING_DICT:
            return True
        else:
            return False

    def get_state_string(self):
        """
        Get string representation of current state.
        """
        state_string = "\n>> "
        if self.state == s.STATE.HOME:
            state_string += "HOME"
        elif self.state == s.STATE.VIEW:
            state_string += "VIEW"
        elif self.state == s.STATE.SELECTING_DICT:
            state_string += "EDIT (SELECT DICTIONARY)"
        elif self.state == s.STATE.EDITING_DICT:
            state_string += f"EDITING (DICTIONARY) >> {self.editing_dictionary}\n"
        elif self.state == s.STATE.MESH:
            state_string += "MESH"
        elif self.state == s.STATE.POST:
            state_string += "POSTPROCESSING"

        return state_string


