import entities
import level
import items
import map
import storyline
from level import Tile
import json
from map import Map
from time import sleep
# Util function for clearing console

with open("Tile_data.json") as f:
    _tile_data = json.load(f)

with open("monster_data.json") as f:
    _monster_data = json.load(f)

with open("item_data.json") as f:
    _item_data = json.load(f)


def clear_console():
    print("\033c", end="", flush=True)


class Game:

    def __init__(self):
        self.map = map.Map()
        self.storyline = storyline.Storyline()
        self.tile_list = []
        self.monsters_list = []
        self.items_list = []
        self.player = entities.Player("", health=100, aura=0, position=[1, 1])
        self.map = Map()

        # TODO: read tile data from storyline and populate level tilelist

    def create_tiles(self):
        for i in range(400):
            y = i // 20 + 1
            x = i % 20 + 1

            for _tile in _tile_data:
                if _tile["position"] == [x, y]:
                    self.tile_list.append(
                        Tile(_tile["position"], _tile["description"]))

            self.tile_list.append(Tile([x, y], "Empty Tile"))

    def initialise_monsters(self):
        for _monster in _monster_data:
            monster = entities.Monsters(_monster["name"], _monster["health"],
                                        [], _monster["damage"],
                                        _monster["description"])
            self.monsters_list.append(monster)

    def initialise_items(self):

        for _item in _item_data:
            if _item["type"] == "HealthPotion":
                item = items.HealthPotion(_item["type"],
                                          _item["name"],
                                          _item["description"],
                                          player=self.player,
                                          effect=_item["health_gain"])

            elif _item["type"] == "AuraPotion":
                item = items.AuraPotion(_item["type"],
                                        _item["name"],
                                        _item["description"],
                                        player=self.player,
                                        effect=_item["aura_gain"])

            else:
                item = items.Weapon(_item["type"],
                                    _item["name"],
                                    _item["description"],
                                    player=self.player,
                                    effect=_item["damage"])

            self.items_list.append(item)

    def start(self):
        self.create_tiles()
        self.initialise_monsters()
        self.initialise_items()
        self.level = level.Level(self.tile_list, self.monsters_list,
                                 self.items_list)
        self.level.spawn_BigBoss()
        self.level.spawn_monsters()
        self.level.spawn_items()
        self.storyline.do_intro()
        name = input("Brave adventurer! What is your name? \n")
        self.player.name = name

    def win(self):
        return self.level.BigBoss.dead()

    def lose(self):
        return self.player.dead()

    def get_options(self) -> list[str]:
        """Returns player's current options as a list of strs"""
        move_options = ["W ", "A ", "S ", "D "]
        combat_options = ["Z X (item number)\n"]
        inventory_options = ["V ", "R ", "P ", "help "
                             "quit "]

        return move_options + combat_options + inventory_options

    def help(self):
        move_options = [
            "To move up, enter W\n", "To move down, enter S\n",
            "To move left, enter A\n", "To move right, enter D\n"
        ]
        combat_options = [
            "To use Item, enter the item number\n",
            "To Punch (5 Damage), enter Z\n", "To kick(10 Damage), enter X\n"
        ]
        inventory_options = [
            "To view Item, enter V, followed by the item number\n",
            "To Drop Item, enter R, followed by the item number\n",
            "To pick up Item, enter P\n"
        ]
        for x in (move_options + combat_options + inventory_options +
                  ["To Quit, enter 'quit'\n"]):
            print(x)
        sleep(5)

    def prompt_player(self, options):
        choice = input(options)
        return choice

    def move(self, choice):

        check = self.player.move(choice)
        if check == "invalid":
            print("This tile does not exist, try moving to another tile")
            sleep(1)
            return 'invalid'

    def use_item(self, choice):
        if int(choice) > len(self.player.inventory):
            print("Item not in inventory")
            sleep(1)
            return 'invalid'
        item = self.player.inventory[int(choice) - 1]
        if item.get_type() == "HealthPotion" or item.get_type(
        ) == "AuraPotion":
            self.player.use_item(
                int(choice) - 1,
                self.get_player_tile().get_monster())
            self.player.remove_item(int(choice) - 1)
            print(f'{item.get_name()} used and removed')
            sleep(1)
        else:
            if self.get_player_tile().get_monster() is not None:
                self.player.use_item(
                    int(choice) - 1,
                    self.get_player_tile().get_monster())
                self.player.remove_item(int(choice) - 1)
                print(f'{item.get_name()} used and removed')
                sleep(1)
            else:
                print("No monster on tile")
                sleep(1)
                return 'invalid'

    def punch(self):
        if self.get_player_tile().get_monster() is not None:
            self.player.punch(self.get_player_tile().get_monster())
        else:
            print("No monster on tile")
            sleep(1)
            return 'invalid'

    def kick(self):
        if self.get_player_tile().get_monster() is not None:
            self.player.kick(self.get_player_tile().get_monster())
        else:
            print("No monster on tile")
            sleep(1)
            return 'invalid'

    def view_item(self):
        x = input("Enter Item number ")
        if x.isnumeric() is False:
            print("Invalid Input")
            sleep(1)
            return 'invalid'
        x = int(x)
        if int(x) > len(self.player.inventory):
            print("Item not in inventory")
            sleep(1)
            return 'invalid'
        item = self.player.inventory[x - 1]
        item.display_item()
        sleep(5)

    def drop_item(self):
        x = input("Enter Item number ")
        if x.isnumeric() is False:
            print("Invalid Input")
            sleep(1)
            return 'invalid'
        x = int(x)
        if int(x) > len(self.player.inventory):
            print("Item not in inventory")
            sleep(1)
            return 'invalid'
        item = self.player.inventory[x - 1]
        self.player.remove_item(x)
        print(f'{item.get_name()} removed')
        sleep(1)

    def pick_up_item(self):
        player_tile = self.get_player_tile()
        tile_item = player_tile.get_item()
        if tile_item is not None:
            self.player.add_item(tile_item)
            player_tile.set_item(None)
            print(f'{tile_item.get_name()} added')
            sleep(1)
        else:
            print("No item on tile")
            sleep(1)
            return 'invalid'

    def enter(self, choice: str):
        if choice in "WASDwasd":
            self.move(choice)
        elif choice.isnumeric():
            self.use_item(choice)
        elif choice in "Zz":
            self.punch()
        elif choice in "Xx":
            self.kick()
        elif choice in "Vv":
            self.view_item()
        elif choice in "Rr":
            self.drop_item()
        elif choice in "Pp":
            self.pick_up_item()
        elif choice in "Hh" or choice.lower() == "help":
            self.help()
        elif choice.lower() == 'quit':
            self.player.health = 0
        else:
            print("This is not an option, enter again")
            sleep(1)
            return 'invalid'

        if self.get_player_tile().get_monster() is not None:
            self.damaged_by_monster()
            self.siphon()

    def show_status(self) -> None:
        """Display player's current status"""

        player_tile = self.get_player_tile()
        player_position = player_tile.get_position()
        player_tile_description = player_tile.get_description()
        tile_item = player_tile.get_item()
        tile_monster = player_tile.get_monster()
        player_inventory = self.get_player_inventory()
        player_health = self.get_player_health()
        player_aura = self.get_player_aura()
        print("\n")
        print(
            f'Your Name: {self.player.get_name()} \nYour Health: {player_health} \nYour Aura: {player_aura} \nYour position: {player_position}, {player_tile_description} \nYour Inventory: {player_inventory}\n'
        )
        if tile_item is not None:
            print("There's an Item on this Tile\n")
            tile_item.display_item()
        else:
            print("There is no item on this Tile\n")

        if tile_monster is not None:
            print("There's a Monster on this Tile\n")
            tile_monster.display_monster()
        else:
            print("There is no Monster on this Tile\n")

        self.map.set_player_position(self.get_player_position()[0] - 1,
                                     self.get_player_position()[1] - 1)

        if tile_item is not None:
            self.map.set_item_position(self.get_player_position()[0] - 1,
                                       self.get_player_position()[1] - 1)

        if tile_monster is not None:
            self.map.set_monsters_position(self.get_player_position()[0] - 1,
                                           self.get_player_position()[1] - 1)

        self.map.display_map()

    def siphon(self):
        player_tile = self.get_player_tile()
        if player_tile.get_monster().dead():
            self.player.gain_health(100)
            self.player.gain_aura(10)
            player_tile.set_monster(None)
            print("You have killed the monster and gained 100 health")
            sleep(1)

    def damaged_by_monster(self):
        player_tile = self.get_player_tile()
        tile_monster = player_tile.get_monster()
        if not tile_monster.dead() and not self.player.dead():
            self.player.lose_health(tile_monster.get_damage())

    def get_player_position(self):
        return self.player.get_position()

    def get_player_tile(self):
        for tile in self.tile_list:
            if self.get_player_position() == tile.get_position():
                return tile
        else:
            return self.tile_list[0]

    def get_player_inventory(self):
        name_inventory = {}
        inventory = self.player.get_inventory()
        for item in inventory:
            name_inventory[inventory.index(item) + 1] = item.get_name()
        return name_inventory

    def get_player_health(self):
        return self.player.get_health()

    def get_player_aura(self):
        return self.player.get_aura()
