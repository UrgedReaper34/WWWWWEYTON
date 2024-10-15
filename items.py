class Item:

    def __init__(self, type, name, description, effect):
        self.type = type
        self.name = name
        self.description = description
        self.effect = effect

    def as_dict(self) -> dict:
        return {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "effect": self.effect
        }

    def display_item(self):
        print(f'Item Type: {self.type}')
        print(f'Item Name: {self.name}')
        print(f'Item Description: {self.description}')
        if self.type == "HealthPotion":
            print(f'Health Gain: {self.effect}')
        elif self.type == "AuraPotion":
            print(f'Aura Gain: {self.effect}')
        elif self.type == "Weapon":
            print(f'Damage: {self.effect}')


class Potion(Item):
    """Potions are items with effects that apply to the user only."""


class HealthPotion(Potion):
    """Health potions are potions that heal the user."""


class AuraPotion(Potion):
    """Aura potions are potions that increase the user's aura."""


class Weapon(Item):

    def as_dict(self) -> dict:
        return {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "damage": self.effect
        }


def create_item(data: dict) -> Item:
    """Generic factory function for items; uses multiple dispatch to determine
    appropriate factory function to call.
    """
    if data["type"] == "HealthPotion":
        return create_health_potion(data)
    elif data["type"] == "AuraPotion":
        return create_aura_potion(data)
    elif data["type"] == "Weapon":
        return create_weapon(data)


def create_health_potion(data: dict) -> HealthPotion:
    """Factory function for health potions."""
    return HealthPotion(data["name"], data["health"], data["description"],
                        data["effect"])


def create_aura_potion(data: dict) -> AuraPotion:
    """Factory function for aura potions."""
    return AuraPotion(data["name"], data["aura"], data["description"],
                      data["effect"])


def create_weapon(data: dict) -> Weapon:
    """Factory function for weapons."""
    return Weapon(data["name"], data["damage"], data["description"],
                  data["damage"])
