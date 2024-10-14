class Item:

    def __init__(self, type, name, description, player, effect):
        self.type = type
        self.name = name
        self.description = description
        self.player = player
        self.effect = effect

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_type(self):
        return self.type

    def get_effect(self):
        return self.effect


class HealthPotion(Item):

    def __init__(self, type, name, description, player, effect):
        super().__init__(type, name, description, player, effect)

    def use_item(self, monster):
        self.player.gain_health(self.effect)

    def display_item(self):
        print(f'Item Type: {self.get_type()}')
        print(f'Item Name: {self.get_name()}')
        print(f'Item Description: {self.get_description()}')
        if self.get_type() == "HealthPotion":
            print(f'Health Gain: {self.get_effect()}')


class AuraPotion(Item):

    def __init__(self, type, name, description, player, effect):
        super().__init__(type, name, description, player, effect)

    def use_item(self, monster):
        self.player.gain_aura(self.effect)

    def display_item(self):
        print(f'Item Type: {self.get_type()}')
        print(f'Item Name: {self.get_name()}')
        print(f'Item Description: {self.get_description()}')
        if self.get_type() == "AuraPotion":
            print(f'Aura Gain: {self.get_effect()}')


class Weapon(Item):

    def __init__(self, type, name, description, player, effect):
        super().__init__(type, name, description, player, effect)

    def use_item(self, monster):
        monster.take_damage(self.effect * (1 + self.player.aura / 100))

    def display_item(self):
        print(f'Item Type: {self.get_type()}')
        print(f'Item Name: {self.get_name()}')
        print(f'Item Description: {self.get_description()}')
        if self.get_type() == "Weapon":
            print(f'Damage: {self.get_effect()}\n')
