def get_options(self) -> list[str]:
        """Returns player's current options as a list of strs"""
        move_options = ["w", "a", "s", "d"]
        combat_options = ["z", "x"]
        item_options = [str(i) for i in range(10)]
        inventory_options = ["v", "r", "p", "help", "quit"]
        return move_options + combat_options + item_options + inventory_options

"""command.py

This module contains constants representing possible player inputs, and the commands they represent.
"""

# Commands are represented as lowercase letters or digits
MOVE_UP = "w"
MOVE_DOWN = "s"
MOVE_LEFT = "a"
MOVE_RIGHT = "d"
PUNCH = "z"
KICK = "x"
USE_ITEM = "u"
VIEW_ITEM = "v"
DROP_ITEM = "r"
PICKUP_ITEM = "p"
HELP_SHORT = "h"
HELP_FULL = "help"
QUIT = "quit"

MOVE = [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]
COMBAT = [PUNCH, KICK]
INVENTORY = [USE_ITEM, VIEW_ITEM, DROP_ITEM, PICKUP_ITEM]
HELP = [HELP_SHORT, HELP_FULL]
SYSTEM = [HELP_SHORT, HELP_FULL, QUIT]

ALL_COMMANDS = MOVE + COMBAT + INVENTORY + SYSTEM
