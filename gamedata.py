import json


with open("Tile_data.json") as f:
    tiles = json.load(f)

with open("monster_data.json") as f:
    monsters = json.load(f)

with open("item_data.json") as f:
    items = json.load(f)

with open("player_data.json") as f:
    player = json.load(f)["player"]
