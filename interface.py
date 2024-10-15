import time

ESC = "\033c"


def clear():
    print("\033c", end="", flush=True)

def linebreak():
    print()

def short_pause():
    time.sleep(1)

def medium_pause():
    time.sleep(3)

def long_pause():
    time.sleep(5)

def show_help():
    print("To move up, enter W")
    print("To move down, enter S")
    print("To move left, enter A")
    print("To move right, enter D")
    print("To use Item, enter the item number")
    print("To Punch (5 Damage), enter Z")
    print("To kick(10 Damage), enter X")
    print("To view Item, enter V, followed by the item number")
    print("To Drop Item, enter R, followed by the item number")
    print("To pick up Item, enter P")
    print("To Quit, enter 'quit'")
    long_pause()

def alert_invalid_input():
    print("Invalid Input")
    short_pause()

def alert_invalid_item():
    print("Item not in inventory")
    short_pause()

def alert_invalid_option():
    print("This is not an option, enter again")
    short_pause()

def alert_invalid_tile():
    print("This tile does not exist, try moving to another tile")
    short_pause()

def prompt_name() -> str:
    return input("Brave adventurer! What is your name? \n")

def prompt_item_number() -> str:
    return input("Enter Item number ")

def prompt_player_choice(options: list[str]) -> str:
    optionstr = " ".join(options)
    choice = input(optionstr)
    while choice not in options:
        alert_invalid_option()
        choice = input(optionstr)
    return choice

def show_player_status(status: dict) -> None:
    linebreak()
    print(f"Name: {status['name']}")
    print(f"Health: {status['health']}")
    print(f"Aura: {status['aura']}")
    print(f"Position: {status['position']}")
    print(f"Inventory: {status['inventory']}")

def show_tile_status(status: dict) -> None:
    if status["item"]:
        print("There's an Item on this Tile")
        for label, value in status["item"].items():
            print(f"Tile {label}: {value}")
    else:
        print("There is no item on this Tile")
    print()
    if status["monster"]:
        print("There's a Monster on this Tile")
        for label, value in status["monster"].items():
            print(f"Monster {label}: {value}")
    else:
        print("There is no Monster on this Tile")
    print()

def report_no_monster():
    print("No monster on tile")
    short_pause()

def report_monster_killed():
    print("You have killed the monster and gained 100 health")

def report_tile_item_picked_up(item: str | None):
    if item:
        print(f"{item} added")
    else:
        print("No item on tile")
    short_pause()

def report_player_item_dropped(item: str):
    print(f'{item} removed')
    short_pause()

def report_player_item_used(item: str):
    print(f'{item} used and removed')
    short_pause()