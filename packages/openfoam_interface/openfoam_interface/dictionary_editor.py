import json
import os
from datetime import datetime

__all__ = ["DictionaryEditor"]

class DictionaryEditor:
    """
    A class for editing dictionaries in the OpenFOAM Interface.
    
    Attributes:
        project_dir (str): The directory of the OpenFOAM project.
        main_dictionary (dict): The main dictionary being edited.
        edit_history (dict): A dictionary storing edit history.
        history (dict): A dictionary storing the latest and older versions of edits.
        latest_version (dict): The latest version of edits.
        older_versions (dict): Older versions of edits.
    """

    def __init__(self, project_dir):
        """
        Initialize the DictionaryEditor object.

        Args:
            project_dir (str): The directory of the OpenFOAM project.
        """
        self.project_dir = project_dir
        self.main_dictionary = {}
        self.edit_history = {}
        self.history = {}
        self.latest_version = {}
        self.older_versions = {}

    def edit(self, dictionary):
        """
        Set the main dictionary to be edited.

        Args:
            dictionary (dict): The dictionary to be edited.
        """
        self.main_dictionary = dictionary

    def make_temporary_edit(self, dict_name, keys, value):
        """
        Make a temporary edit to the dictionary.

        Args:
            dict_name (str): The name of the dictionary being edited.
            keys (str): The keys specifying the location of the value in the dictionary.
            value (str): The new value to be assigned.

        Returns:
            dict: The modified dictionary.
        """
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        user = os.getlogin()

        try:
            keys = keys.strip().split(".")
            command = "self.main_dictionary"
            for key in keys:
                if key.isdigit():
                    command += f"[{key}]"
                else:
                    command += f"[\'{key}\']"
            command += f" = {value}"
            exec(command, globals(), locals())
            command = command.replace("self.main_dictionary", "")
            print(f"Added: {dict_name+command.split('=')[0].strip()} = {command.split('=')[1].strip()}")
            self.edit_history[timestamp] = {"dict_name": dict_name, "key": keys, "value": command.split("=")[1].strip(), "user": user}

        except Exception as e:
            print(f"Error: {e}. Invalid edit. Try again.")

        return self.main_dictionary

    def save_edits(self):
        """
        Save the temporary edits to the main dictionary and update edit history.

        Returns:
            dict: The main dictionary with edits applied.
        """
        for edit in self.edit_history.keys():
            self._add_to_history(edit)
        self.save_history_to_file("_history.json")
        return self.main_dictionary

    def _add_to_history(self, timestamp):
        """
        Add a temporary edit to the edit history.

        Args:
            timestamp (str): The timestamp of the edit.
        """
        if timestamp in self.latest_version.keys():
            self.older_versions[timestamp] = self.latest_version[timestamp]
        self.latest_version[timestamp] = self.edit_history[timestamp]

    def save_history_to_file(self, filename):
        """
        Save the edit history to a JSON file.

        Args:
            filename (str): The name of the JSON file.
        """
        self.history = {"latest_version": self.latest_version, "older_versions": self.older_versions}
        with open(filename, "w") as file:
            json.dump(self.history, file)

    def load_history_from_file(self, filename):
        """
        Load edit history from a JSON file.

        Args:
            filename (str): The name of the JSON file.
        """
        with open(filename, "r") as file:
            self.history = json.load(file)

    def import_history(self, dictionaries):
        """
        Import edit history and apply changes to dictionaries.

        Args:
            dictionaries (dict): The dictionaries to be updated.
        """
        print("Checking for history of dictionary changes...")
      
        history_file = os.path.join(self.project_dir, "_history.json")
       
        if os.path.isfile(history_file):
            f = open(history_file)
            self.history = json.load(f)
            print("History found. Importing changes...")

        else:
            self.history = {"latest_version": {}, "older_versions": {}}
            f = open(history_file, "w")
            json.dump(self.history, f)

        self.latest_version = self.history["latest_version"]
        self.older_versions = self.history["older_versions"]

        if len(self.latest_version.keys()) > 0:
            for timestamp in self.latest_version.keys():
                dict_name = self.latest_version[timestamp]["dict_name"]
                keys = self.latest_version[timestamp]["key"]
                value = self.latest_version[timestamp]["value"]

                keystring = "dictionaries"
                keystring += f"[\'{dict_name}\']"
                for key in keys:
                    if key.isdigit():
                        keystring += f"[{key}]"
                    else:
                        keystring += f"[\'{key}\']"

                edit = f"{keystring} = {value}"
                exec(edit, globals(), locals())

        return dictionaries

    def are_you_sure(self, action):
        if self.edit_history == {}:
            return True

        check = input("Are you sure you want to " + action + "? (y/n): ").strip().lower()
        if check == "y":
            self.save_changes()
            return True
        elif check == "n":
            return False
        else:
            self.are_you_sure(action)

    def save_changes(self):
        check = input("Save changes? (y/n): ").strip().lower()
        if check == "y":
            self.save_edits()
            return True
        elif check == "n":
            return False
        else:
            self.save_changes()


