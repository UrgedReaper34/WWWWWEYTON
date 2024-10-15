import items


class Entity:

    def __init__(self, name, health, position):
        self.name = name
        self.health = health
        self.position = position

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health

    def gain_health(self, gained_health):
        self.health += gained_health

    def lose_health(self, damage):
        self.health -= damage

    def take_damage(self, damage):
        self.health -= damage

    def get_position(self):
        return self.position

    def dead(self):
        return self.health <= 0

    def move(self, move):

        if move in "Ww":
            if self.get_position()[1] <= 1:
                return "invalid"
            else:
                self.position[1] -= 1
                return self.get_position()

        elif move in "Aa":
            if self.get_position()[0] <= 1:
                return "invalid"
            else:
                self.position[0] -= 1
                return self.get_position()

        elif move in "Ss":
            if self.get_position()[1] >= 20:
                return "invalid"
            else:
                self.position[1] += 1
                return self.get_position()

        elif move in "Dd":
            if self.get_position()[0] >= 20:
                return "invalid"
            else:
                self.position[0] += 1
                return self.get_position()

    def status(self) -> dict:
        return {
            "name": self.name,
            "health": self.health,
            "position": self.position
        }


class Player(Entity):

    def __init__(self, name: str, health: int, aura: int, position, inventory=[]):
        super().__init__(name, health, position)
        self.inventory = inventory
        self.aura = aura

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

    def punch(self, monster: Monster) -> None:
        monster.take_damage(5 * (1 + self.aura / 100))

    def kick(self, monster: Monster) -> None:
        monster.take_damage(10 * (1 + self.aura / 100))

    def use_item(self, item: items.Item, monster: Monster) -> None:
        item = self.inventory[item]
        item.use_item(monster)

    def get_inventory(self) -> list[items.Item]:
        return self.inventory

    def status(self) -> dict:
        statusdata = super().status()
        statusdata["aura"] = self.aura
        statusdata["inventory"] = [item.name for item in self.inventory]
        return statusdata


class Monster(Entity):

    def __init__(self, name: str, health: int, position, damage: int, description: str):
        super().__init__(name, health, position)
        self.damage = damage
        self.description = description

    def get_damage(self) -> int:
        return self.damage

    def set_damage(self, damage: int) -> int:
        self.damage = damage

    def get_description(self) -> str:
        return self.description

    def display_monster(self) -> None:
        print(f'Monster Name: {self.get_name()}')
        print(f'Monster Health: {self.get_health()}')
        print(f'Monster Description: {self.get_description()}')
        print(f'Damage: {self.get_damage()}\n')


# test
# person1 = Player("Lleyton",100000,10,[1,2])

# adj_tiles = {
#     "UP" : [1,3],
#     "DOWN" : [1,1],
#     "RIGHT" : [2,2],
#     "LEFT" : None
# }
# print(person1.move("RIGHT",adj_tiles))
