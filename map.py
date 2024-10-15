"""map.py

This module defines the map and coordinate interface of the game.
"""
import mapsymbol as sym

# Entity coordinates are represented as a (x, y) 2-element tuple
Position = tuple[int, int]


def make_grid(width: int, height: int, char: str) -> list[list[str]]:
    """Return a grid of the given width and height, filled with the given
    character.
    """
    return [[char for _ in range(width)] for _ in range(height)]


class Map:
    """Encapsulates map symbols, grid coordinates, and positions of player
    and boss.
    """
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = make_grid(width, height, char=sym.EMPTY)
        self.player_position: Position = (0, 0)
        self.final_boss_position: Position = (19, 19)
        player_x, player_y = self.player_position
        self.set_grid(player_x, player_y, sym.PLAYER)
        boss_x, boss_y = self.final_boss_position
        self.set_grid(boss_x, boss_y, sym.BOSS)

    def get_grid(self, x: int, y: int) -> str:
        """Return the character at the given position."""
        return self.grid[y][x]

    def set_grid(self, x: int, y: int, char: str) -> None:
        """Set the character at the given position."""
        self.grid[y][x] = char

    def is_valid_coord(self, x: int, y: int) -> bool:
        """Check if the given coordinates are within the map boundaries.
        Returns a bool indicating whether the coordinates are valid.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_player_position(self) -> Position:
        return self.player_position

    def set_player_position(self, new_x: int, new_y: int) -> None:
        if not self.is_valid_coord(new_x, new_y):
            print(f"Position ({new_x}, {new_y}) is out of bounds!")
            return
        old_x, old_y = self.player_position
        if self.grid[old_y][old_x] == sym.PLAYER:
            self.grid[old_y][old_x] = sym.EMPTY
        self.player_position = (new_x, new_y)
        self.grid[new_y][new_x] = sym.PLAYER

    def set_monsters_position(self, x: int, y: int) -> None:
        """Put a monster at the given position."""
        if not self.is_valid_coord(x, y):
            print(f"Position ({x}, {y}) is out of bounds!")
            return
        self.set_grid(x, y, sym.MONSTER)

    def set_item_position(self, x: int, y: int) -> None:
        """Put an item at the given position."""
        if not self.is_valid_coord(x, y):
            print(f"Position ({x}, {y}) is out of bounds!")
            return
        self.set_grid(x, y, sym.ITEM)

    def display_map(self):
        """Prints the current state of the map."""
        for row in self.grid:
            print(' '.join(row))
