import csv

class Map:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
       # print(self.grid)
        self.grid = []
        with open('level1.txt', newline='') as csvfile:
            reader = list(csv.reader(csvfile))
            
            for i in range(0, len(reader)):
                row = reader[i]
                print(type(row))
                print(row)
                self.grid.append([])
                print(f"i: {i}")
                for x in range(0, len(row[0])):
                    
                    self.grid[i].append(row[0][x])
                    
            
        
        self.player_position = [0, 0]  
        self.final_boss_position = [19,19]
        self.grid[self.player_position[1]][self.player_position[0]] = 'P'
        self.grid[self.final_boss_position[1]][self.final_boss_position[0]] = 'B'
        

    def get_player_position(self):
        return self.player_position

    def set_player_position(self, new_x, new_y):
        old_x, old_y = self.player_position
        if self.grid[old_y][old_x] == 'P':
            self.grid[old_y][old_x] = '.'
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.player_position = [new_x, new_y]
            self.grid[new_y][new_x] = 'P'
        else:
            print(f"Position ({new_x}, {new_y}) is out of bounds!")

    def set_monsters_position(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 'M'
        else:
            print(f"Position ({new_x}, {new_y}) is out of bounds!")

    def display_map(self):
        """
        Prints the current state of the map.
        """
        for row in self.grid:
            print(' '.join(row))
