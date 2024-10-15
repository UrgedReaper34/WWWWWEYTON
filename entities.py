"""entities.py

Module containing all entities in the game.
"""

import items

# Positions are represented as a list of two ints
Position = list[int]


class Entity:

    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health

    def get_name(self) -> str:
        return self.name

    def get_health(self) -> int:
        return self.health

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

    def get_aura(self) -> int:
        return self.aura

    def set_aura(self, aura: int):
        self.aura = aura

    def gain_aura(self, aura_gained: int):
        self.aura += aura_gained

    def add_item(self, item: items.Item):
        self.inventory.append(item)

    def remove_item(self, item: items.Item):
        self.inventory.remove(item)

    def punch(self, monster: "Monster") -> None:
        monster.take_damage(int(5 * (1 + self.aura / 100)))

    def kick(self, monster: "Monster") -> None:
        monster.take_damage(int(10 * (1 + self.aura / 100)))

    def use_item(self, item: items.Item, monster: "Monster") -> None:
        item.use_item(monster)

    def get_inventory(self) -> list[items.Item]:
        return self.inventory

    def status(self) -> dict:
        statusdata = super().status()
        statusdata["aura"] = self.aura
        statusdata["inventory"] = [item.name for item in self.inventory]
        return statusdata


class Monster(Entity):

    def __init__(self, name: str, health: int, damage: int,
                 description: str):
        super().__init__(name, health)
        self.damage = damage
        self.description = description

    def get_damage(self) -> int:
        return self.damage

    def set_damage(self, damage: int) -> None:
        self.damage = damage

    def get_description(self) -> str:
        return self.description

    def status(self) -> dict:
        statusdata = super().status()
        statusdata["damage"] = self.damage
        return statusdata

    def display_monster(self) -> None:
        print(f'Monster Name: {self.name}')
        print(f'Monster Health: {self.health}')
        print(f'Monster Description: {self.description}')
        print(f'Damage: {self.damage}\n')


def create_player(data: dict) -> Player:
    return Player(data["name"], data["health"], data["aura"])

def create_monster(data: dict) -> Monster:
    return Monster(data["name"], data["health"], data["damage"], data["description"])

# test
# person1 = Player("Lleyton",100000,10,[1,2])

# adj_tiles = {
#     "UP" : [1,3],
#     "DOWN" : [1,1],
#     "RIGHT" : [2,2],
#     "LEFT" : None
# }
# print(person1.move("RIGHT",adj_tiles))
