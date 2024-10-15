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


class Game:

    def __init__(self):
        self.map = map.Map()
        self.storyline = storyline.Storyline()
        self.level = level.create_level()
        self.tile_list = []
        self.player = entities.create_player(gamedata.player)
        player_x, player_y = gamedata.player["position"]
        self.map.set_player_position(player_x, player_y)

        # TODO: read tile data from storyline and populate level tilelist

    def create_tiles(self):
        for tiledata in gamedata.tiles:
            x, y = tiledata["position"]
            self.level.set_tile(
                x, y,
                level.create_tile(tiledata)
            )

    def start(self):
        self.create_tiles()
        self.level = level.create_level()
        self.level.spawn_BigBoss()
        self.level.spawn_monsters(
            [
                entities.create_monster(monsterdata)
                for monsterdata in gamedata.monsters
            ]
        )
        self.level.spawn_items(
            [
                items.create_item(itemdata)
                for itemdata in gamedata.items
            ]
        )
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

    def get_player_position(self) -> map.Position:
        return self.map.player_position

    def get_player_tile(self) -> level.Tile | None:
        x, y = self.get_player_position()
        return self.level.get_tile(x, y)

    def get_tile_monster(self) -> entities.Monster | None:
        """Returns the monster on the current tile"""
        tile = self.get_player_tile()
        if not tile:
            return None
        return tile.monster

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

    def punch(self) -> bool:
        """Execute a punch"""
        monster = self.get_tile_monster()
        if not monster:
            interface.report_no_monster()
            return False
        self.player.punch(monster)
        return True

    def kick(self) -> bool:
        """Execute a kick"""
        monster = self.get_tile_monster()
        if not monster:
            interface.report_no_monster()
            return False
        self.player.kick(monster)
        return True

    def use_item(self, user: entities.Player, item: items.Item, target: entities.Entity | None = None) -> None:
        """Use the item on the target"""
        if isinstance(item, items.Potion):
            if isinstance(item, items.HealthPotion):
                user.gain_health(item.effect)
            elif isinstance(item, items.AuraPotion):
                user.gain_aura(item.effect)
        elif isinstance(item, items.Weapon):
            assert target is not None, "Target must be specified for weapons"
            target.take_damage(int(item.effect * (1 + user.aura / 100)))
        else:
            raise ValueError(f"Invalid item type: {type(item)}")

    def menu_use_item(self) -> bool:
        """Use the item in the player's inventory according to their choice"""
        tile = self.get_player_tile()
        item = interface.prompt_item_choice(self.player.inventory)
        if not item:
            return False
        elif isinstance(item, items.Potion):
            self.use_item(self.player, item)
            self.player.remove_item(item)
            interface.report_player_item_used(item.name)
        elif isinstance(item, items.Weapon):
            if not tile or not tile.monster:
                interface.report_no_monster()
                return False
            self.use_item(self.player, item, tile.monster)
            interface.report_player_item_used(item.name)
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
        tile = self.get_player_tile()
        if not tile or not tile.item:
            interface.report_no_item()
            return False
        self.player.add_item(tile.item)
        tile.remove_item()
        interface.report_tile_item_picked_up(tile.item.name)
        return True

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

        monster = self.get_tile_monster()
        if monster:
            self.damaged_by_monster()
            self.siphon()
        return result

    def show_status(self) -> None:
        """Display player's current status"""
        tile = self.get_player_tile()
        player_status = self.player.status()
        # On the map, positions are shown with origin position (1, 1)
        # so x and y coords need to be incremented
        player_x, player_y = self.get_player_position()
        player_status["position"] = (player_x + 1, player_y + 1)
        if not tile:
            player_status["tile_description"] = "Empty tile"
            tile_status = {"item": None, "monster": None}
        else:
            player_status["tile_description"] = tile.description
            tile_status = {
                "item": tile.item and tile.item.as_dict(),
                "monster": tile.monster and tile.monster.status()
            }
        interface.show_player_status(player_status)
        interface.show_tile_status(tile_status)
        self.map.display_map()

    def siphon(self):
        tile = self.get_player_tile()
        monster = self.get_tile_monster()
        if (tile and monster and monster.dead()):
            self.player.gain_health(100)
            self.player.gain_aura(10)
            tile.remove_monster()
            interface.report_monster_killed()
            interface.short_pause()

    def damaged_by_monster(self):
        monster = self.get_tile_monster()
        if monster and not monster.dead() and not self.player.dead():
            self.player.lose_health(monster.damage)
