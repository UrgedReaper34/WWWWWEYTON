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
USE_ITEM_1 = "0"
USE_ITEM_2 = "1"
USE_ITEM_3 = "2"
USE_ITEM_4 = "3"
USE_ITEM_5 = "4"
USE_ITEM_6 = "5"
USE_ITEM_7 = "6"
USE_ITEM_8 = "7"
USE_ITEM_9 = "8"
USE_ITEM_10 = "9"
VIEW_ITEM = "v"
DROP_ITEM = "r"
PICKUP_ITEM = "p"
HELP_SHORT = "h"
HELP_FULL = "help"
QUIT = "quit"

MOVE = [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]
COMBAT = [PUNCH, KICK]
USE_ITEM = [USE_ITEM_1, USE_ITEM_2, USE_ITEM_3, USE_ITEM_4, USE_ITEM_5, USE_ITEM_6, USE_ITEM_7, USE_ITEM_8, USE_ITEM_9, USE_ITEM_10]
INVENTORY = [VIEW_ITEM, DROP_ITEM, PICKUP_ITEM]
HELP = [HELP_SHORT, HELP_FULL]
SYSTEM = [HELP_SHORT, HELP_FULL, QUIT]

ALL_COMMANDS = MOVE + COMBAT + USE_ITEM + INVENTORY + SYSTEM
