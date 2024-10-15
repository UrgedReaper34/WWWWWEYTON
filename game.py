import entities
import gamedata
import level
import interface
import items
import map
import storyline
from level import Tile
from map import Map
from time import sleep


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

            for _tile in gamedata.tiles:
                if _tile["position"] == [x, y]:
                    self.tile_list.append(
                        Tile(_tile["position"], _tile["description"]))

            self.tile_list.append(Tile([x, y], "Empty Tile"))

    def initialise_monsters(self):
        for _monster in gamedata.monsters:
            monster = entities.Monsters(_monster["name"], _monster["health"],
                                        [], _monster["damage"],
                                        _monster["description"])
            self.monsters_list.append(monster)

    def initialise_items(self):

        for _item in gamedata.items:
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
        name = interface.prompt_name()
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

    def move(self, choice):

        check = self.player.move(choice)
        if check == "invalid":
            interface.alert_invalid_tile()
            return 'invalid'

    def use_item(self, choice):
        if int(choice) > len(self.player.inventory):
            interface.alert_invalid_item()
            return 'invalid'
        item = self.player.inventory[int(choice) - 1]
        if item.get_type() == "HealthPotion" or item.get_type(
        ) == "AuraPotion":
            self.player.use_item(
                int(choice) - 1,
                self.get_player_tile().get_monster())
            self.player.remove_item(int(choice) - 1)
            interface.report_player_item_used(item.name)
        else:
            if self.get_player_tile().get_monster() is not None:
                self.player.use_item(
                    int(choice) - 1,
                    self.get_player_tile().get_monster())
                self.player.remove_item(int(choice) - 1)
                interface.report_player_item_used(item.name)
            else:
                interface.report_no_monster()
                return 'invalid'

    def punch(self):
        if self.get_player_tile().get_monster() is not None:
            self.player.punch(self.get_player_tile().get_monster())
        else:
            interface.report_no_monster()
            return 'invalid'

    def kick(self):
        if self.get_player_tile().get_monster() is not None:
            self.player.kick(self.get_player_tile().get_monster())
        else:
            interface.report_no_monster()
            return 'invalid'

    def view_item(self):
        x = input("Enter Item number ")
        if x.isdecimal() is False:
            interface.alert_invalid_input()
            return 'invalid'
        x = int(x)
        if int(x) > len(self.player.inventory):
            interface.alert_invalid_item()
            return 'invalid'
        item = self.player.inventory[x - 1]
        item.display_item()
        sleep(5)

    def drop_item(self):
        x = interface.prompt_item_number()
        if x.isdecimal() is False:
            interface.alert_invalid_input()
            return 'invalid'
        x = int(x)
        if int(x) > len(self.player.inventory):
            interface.alert_invalid_item()
            return 'invalid'
        item = self.player.inventory[x - 1]
        self.player.remove_item(x)
        interface.report_player_item_dropped(item.name)

    def pick_up_item(self):
        player_tile = self.get_player_tile()
        tile_item = player_tile.get_item()
        if tile_item:
            self.player.add_item(tile_item)
            player_tile.set_item(None)
        interface.report_tile_item_picked_up(tile_item.name if tile_item else None)
        if tile_item:
            return 'invalid'

    def enter(self, choice: str):
        choice = choice.lower()
        if choice in "wasd":
            self.move(choice)
        elif choice.isdecimal():
            self.use_item(choice)
        elif choice in "z":
            self.punch()
        elif choice in "x":
            self.kick()
        elif choice in "v":
            self.view_item()
        elif choice in "r":
            self.drop_item()
        elif choice in "p":
            self.pick_up_item()
        elif choice in "h" or choice.lower() == "help":
            interface.show_help()
        elif choice.lower() == 'quit':
            self.player.health = 0
        else:
            interface.alert_invalid_option()
            return 'invalid'

        if self.get_player_tile().get_monster() is not None:
            self.damaged_by_monster()
            self.siphon()

    def show_status(self) -> None:
        """Display player's current status"""
        player_tile = self.get_player_tile()
        tile_item = player_tile.get_item()
        tile_monster = player_tile.get_monster()
        player_status = self.player.status()
        player_status["tile_description"] = player_tile.get_description()
        interface.show_player_status(player_status)
        tile_status = {
            "item": tile_item.as_dict() if tile_item else None,
            "monster": tile_monster.as_dict() if tile_monster else None
        }
        interface.show_tile_status(tile_status)

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
            interface.report_monster_killed()
            interface.short_pause()

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
