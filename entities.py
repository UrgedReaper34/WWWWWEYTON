
class Entity():

    def __init__(self, name, health, aura, position):
        self.name = name
        self.health = health
        self.aura = aura
        self.position = position

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health

    def gain_health(self, gained_health):
        self.health += gained_health

    def take_damage(self, damage):
        self.health -= damage
    
    def get_position(self):
        return self.position
    
    def move(self, move, adjacent_tiles):
        
        if move == "UP":
            if adjacent_tiles[move] is None:
                return "invalid"
            else:
                self.position[1] += 1
                return self.get_position()
                
        elif move == "LEFT":
            if adjacent_tiles[move] is None:
                return "invalid"
            else:
                self.position[0] -= 1
                return self.get_position()
            
        elif move == "DOWN":
            if adjacent_tiles[move] is None:
                return "invalid"
            else:
                self.position[1] -= 1
                return self.get_position()
    
            
        elif move == "RIGHT":
            if adjacent_tiles[move] is None:
                return "invalid"
            else:
                self.position[0] += 1
                return self.get_position()
            
    


class Player(Entity):

    def __init__(self, name, health, aura, position,inventory = []):
        super().__init__(name, health, aura, position)
        self.inventory = inventory

    def get_aura(self):
        return self.aura

    def set_aura(self,aura):
        self.aura = aura

    def add_item(self,item):
        self.inventory.append(item)

    def remove_item(self,item):
        self.inventory.remove(item)

    def punch(self, monster):
        monster.take_damage(5)

    def kick(self, monster):
        monster.take_damage(10)

    def use_item(self, item_index, monster):
        item = self.inventory[item_index - 1]
        item.use_item(monster)

    def get_inventory(self):
        return self.inventory

    
class Monster(Entity):
    
    def __init__(self, name, health, aura, position, damage, description, inventory = []):
        super().__init__(name, health, aura, position)
        self.damage = damage
        self.description = description
        self.inventory = inventory
        

    def pickup_item(self,item):
        self.inventory.append(item)

    def get_inventory(self):
        return self.inventory
    
        
class Creature(Entity):

    def __init__(self, name, health, aura, position, damage, description):
        super().__init__(name, health, aura, position)
        self.damage = damage
        self.description = description


    def get_damage(self):
        return self.damage

    def set_damage(self, damage):
        self.damage = damage


# test
# person1 = Player("Lleyton",100000,10,[1,2])

# adj_tiles = {
#     "UP" : [1,3],
#     "DOWN" : [1,1],
#     "RIGHT" : [2,2],
#     "LEFT" : None
# }
# print(person1.move("RIGHT",adj_tiles))
    
    
    
