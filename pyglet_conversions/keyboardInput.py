# this is a shortcut dict for keyboard input

import pygame
from enum import Enum

try:
    from enum import auto
except ImportError:
    def auto():
        global number
        number += 1
        return number

# button enums shared between controller and chars
X = auto()
A = auto()
B = auto()
Y = auto()
L = auto()
R = auto()
SELECT = auto()
START = auto()
RIGHT = auto()
LEFT = auto()
UP = auto()
DOWN = auto()

