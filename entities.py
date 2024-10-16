"""entities.py

Module containing all entities in the game.
"""

import items


class Entity:

    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health

    def gain_health(self, gained_health: int) -> None:
        self.health += gained_health

    def lose_health(self, damage: int) -> None:
        self.health -= damage

    def take_damage(self, damage: int) -> None:
        self.health -= damage

    def dead(self) -> bool:
        return self.health <= 0

    def status(self) -> dict:
        return {
            "name": self.name,
            "health": self.health,
        }


class Player(Entity):

    def __init__(self, name: str, health: int, aura: int):
        super().__init__(name, health)
        self.aura = aura
        self.inventory = []

    def gain_aura(self, aura_gained: int):
        self.aura += aura_gained

    def add_item(self, item: items.Item):
        self.inventory.append(item)

    def remove_item(self, item: items.Item):
        self.inventory.remove(item)

    def status(self) -> dict:
        statusdata = super().status()
        statusdata["aura"] = self.aura
        statusdata["inventory"] = [item.name for item in self.inventory]
        return statusdata


class Monster(Entity):

    def __init__(self, name: str, health: int, damage: int, description: str):
        super().__init__(name, health)
        self.damage = damage
        self.description = description

    def set_damage(self, damage: int) -> None:
        self.damage = damage

    def status(self) -> dict:
        statusdata = super().status()
        statusdata["damage"] = self.damage
        return statusdata


def create_player(data: dict) -> Player:
    return Player(data["name"], data["health"], data["aura"])


def create_monster(data: dict) -> Monster:
    return Monster(data["name"], data["health"], data["damage"],
                   data["description"])


# test
# person1 = Player("Lleyton",100000,10,[1,2])

# adj_tiles = {
#     "UP" : [1,3],
#     "DOWN" : [1,1],
#     "RIGHT" : [2,2],
#     "LEFT" : None
# }
# print(person1.move("RIGHT",adj_tiles))
