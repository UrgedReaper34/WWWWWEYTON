"""game.py

This module contains the Game class, which represents the game state.
"""

import command
import entities
import gamedata
import level
import interface
import items
import map
import storyline
from level import Tile


class Game:

    def __init__(self):
        self.map = map.Map()
        self.storyline = storyline.Storyline()
        self.tile_list = []
        self.monsters_list = []
        self.items_list = []
        self.player = entities.create_player(gamedata.player)
        player_x, player_y = gamedata.player["position"]
        self.map.set_player_position(player_x, player_y)

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
        for monsterdata in gamedata.monsters:
            monster = entities.create_monster(monsterdata)
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
        return command.ALL_COMMANDS

    def move_player(self, move: str) -> bool:
        """Move the player in the given direction.
        Return a boolean indicating whether the player has moved.
        Move is assumed to be a valid move command.
        """
        move = move.lower()
        player_x, player_y = self.get_player_position()
        if move == "w":
            player_y -= 1
        elif move == "s":
            player_y += 1
        elif move == "a":
            player_x -= 1
        elif move == "d":
            player_x += 1
        else:
            raise ValueError(f"Invalid move: {move}")
        if not self.map.is_valid_coord(player_x, player_y):
            return False
        self.map.set_player_position(player_x, player_y)
        return True

    def move(self, choice) -> bool:
        """Move the player according to their choice"""
        done = self.move_player(choice)
        if not done:
            interface.alert_invalid_tile()
            return False
        return True

    def menu_use_item(self) -> bool:
        """Use the item in the player's inventory according to their choice"""
        monster = self.get_player_tile().get_monster()
        item = interface.prompt_item_choice(self.player.inventory)
        if not item:
            return False
        elif (
                monster
                or isinstance(item, (items.HealthPotion, items.AuraPotion))
        ):
            self.player.use_item(item, monster)
            self.player.remove_item(item)
            interface.report_player_item_used(item.name)
        else:
            interface.report_no_monster()
            return False
        return True

    def punch(self) -> bool:
        """Execute a punch"""
        if self.get_player_tile().get_monster() is not None:
            self.player.punch(self.get_player_tile().get_monster())
        else:
            interface.report_no_monster()
            return False
        return True

    def kick(self) -> bool:
        """Execute a kick"""
        if self.get_player_tile().get_monster() is not None:
            self.player.kick(self.get_player_tile().get_monster())
        else:
            interface.report_no_monster()
            return False
        return True

    def menu_view_item(self) -> bool:
        """View the item in the player's inventory according to their choice"""
        item = interface.prompt_item_choice(self.player.inventory)
        if not item:
            return False
        item.display_item()
        interface.long_pause()
        return True

    def menu_drop_item(self) -> bool:
        """Drop the item in the player's inventory"""
        item = interface.prompt_item_choice(self.player.inventory)
        if not item:
            return False
        self.player.remove_item(item)
        interface.report_player_item_dropped(item.name)
        return True

    def pick_up_item(self) -> bool:
        """Pick up the item on the current tile"""
        player_tile = self.get_player_tile()
        tile_item = player_tile.get_item()
        if tile_item:
            self.player.add_item(tile_item)
            player_tile.set_item(None)
        interface.report_tile_item_picked_up(
            tile_item.name if tile_item else None)
        return True if tile_item else False

    def enter(self, choice: str) -> bool:
        """Carry out user choice.
        Returns a bool representing whether the action was carried out.
        Validation should be done before passing to this method.
        """
        choice = choice.lower()
        if choice in command.MOVE:
            result = self.move(choice)
        elif choice == command.PUNCH:
            result = self.punch()
        elif choice == command.KICK:
            result = self.kick()
        elif choice == command.USE_ITEM:
            result = self.menu_use_item()
        elif choice == command.VIEW_ITEM:
            result = self.menu_view_item()
        elif choice == command.DROP_ITEM:
            result = self.menu_drop_item()
        elif choice == command.PICKUP_ITEM:
            result = self.pick_up_item()
        elif choice in command.HELP:
            interface.show_help()
            return True
        elif choice == command.QUIT:
            self.player.health = 0
            return True
        else:
            raise ValueError(f"Invalid choice: {choice}")

        if self.get_player_tile().get_monster() is not None:
            self.damaged_by_monster()
            self.siphon()
        return result

    def show_status(self) -> None:
        """Display player's current status"""
        player_tile = self.get_player_tile()
        tile_item = player_tile.get_item()
        tile_monster = player_tile.get_monster()
        player_status = self.player.status()
        # On the map, positions are shown with origin position (1, 1)
        # so x and y coords need to be incremented
        player_x, player_y = self.get_player_position()
        player_status["position"] = (player_x + 1, player_y + 1)
        player_status["tile_description"] = player_tile.get_description()
        interface.show_player_status(player_status)
        tile_status = {
            "item": tile_item.as_dict() if tile_item else None,
            "monster": tile_monster.as_dict() if tile_monster else None
        }
        # FIX: update tile item and monster position
        interface.show_tile_status(tile_status)

        
        # self.map.set_player_position(self.get_player_position()[0] - 1,
        #                              self.get_player_position()[1] - 1)

        # if tile_item is not None:
        #     self.map.set_item_position(self.get_player_position()[0] - 1,
        #                                self.get_player_position()[1] - 1)

        # if tile_monster is not None:
        #     self.map.set_monsters_position(self.get_player_position()[0] - 1,
        #                                    self.get_player_position()[1] - 1)

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

    def get_player_position(self) -> map.Position:
        return self.map.player_position

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
