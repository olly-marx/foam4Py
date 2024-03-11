"""
state.py

A module that defines the STATE enum for various states used in the pyBindFOAM interface.

Author: Oliver Marx
Email: oliver.j.marx@gmail.com

Description:
    This module defines the STATE enum, which represents the different states
    used in the pyBindFOAM interface.

Usage: 
    The STATE enum is used to manage the state transitions and actions in the interface.

Dependencies:
    None
"""

from enum import Enum

__all__ = ["STATE"]

class STATE(Enum):
    """
    Enum representing the various states of the pyBindFOAM interface.

    Attributes:
        HOME: Represents the home state of the interface.
        VIEW: Represents the state for viewing dictionary contents.
        SELECTING_DICT: Represents the state for selecting a dictionary to edit.
        EDITING_DICT: Represents the state for editing a dictionary.
        MESH: Represents the state for meshing utilities.
        POST: Represents the state for post-processing utilities.
    """
    HOME = 1
    VIEW = 2
    SELECTING_DICT = 3
    EDITING_DICT = 4
    MESH = 5
    POST = 6

