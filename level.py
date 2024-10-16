import random

import entities
import gamedata
import items
import map


class Tile:
    """A tile holds up to one monster and up to one item."""
    def __init__(self, description: str):
        self.description = description
        self.monster = None
        self.item = None

    def remove_monster(self) -> None:
        self.monster = None

    def remove_item(self) -> None:
        self.item = None
    
    def set_monster(self, monster: entities.Monster) -> None:
        self.monster = monster
    
    def set_item(self, item: items.Item) -> None:
        self.item = item


class Level:
    """
    generate new level by the size given
    level_num --> int
    """

    def __init__(self):
        self.tile_map = {}
        # self.monsters_list = monsters_list
        # self.items_list = items_list
        self.BigBoss = entities.create_monster(gamedata.boss)

    def get_tile(self, x: int, y: int) -> Tile | None:
        pos = (x, y)
        if pos not in self.tile_map:
            return None
        return self.tile_map[(x, y)]

    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        pos = (x, y)
        self.tile_map[pos] = tile

    def spawn_BigBoss(self) -> None:
        last_tile = list(self.tile_map.values())[-1]
        last_tile.set_monster(self.BigBoss)

    def spawn_monsters(self, monsters: list[entities.Monster]) -> None:
        """randomly add monsters into tiles"""
        for monster in monsters:
            new_tile = None
            while not new_tile or new_tile.get_monster():
                new_tile = random.choice(list(self.tile_map.values()))
            new_tile.set_monster(monster)

    def spawn_items(self, items: list[items.Item]) -> None:
        """randomly add items into tiles"""
        for item in items:
            new_tile = None
            while not new_tile or new_tile.get_item():
                new_tile = random.choice(list(self.tile_map.values()))
            new_tile.set_item(item)


def create_tile(data: dict) -> Tile:
    return Tile(data["description"])

def create_level() -> Level:
    return Level()