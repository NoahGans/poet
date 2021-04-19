import random
from enviormental_feature import Feature

class World:
    def __init__(self, name):
        self.name = name
        self.size = 10
        self.world = [[[0 for z in range(2)] for x in range(self.size)] for y in range(self.size)] 
        
    def __str__(self):
        return_string = ""
        for i in range(self.size):
            for j in range(self.size):
                return_string += self.world[i][j][0].__str__()
                for k in range(11 - len(self.world[i][j][0].__str__())):
                    return_string += " "
                return_string += " | "
                
            return_string += "\n"   
        return return_string
    
    def printy(self):
        return_string = ""
        for i in range(self.size):
            for j in range(self.size):
                return_string += self.world[i][j][1].__str__()
                for k in range(11 - len(self.world[i][j][1].__str__())):
                    return_string += " "
                return_string += " | "
            return_string += "\n" 
        return return_string

    def set_poet_loc(self, x, y, poet):
        if self.world[x][y][1] != 0:
            return False
        else:
            self.world[x][y][1] = poet
            return True

    def clear_loc(self, x, y):
        self.world[x][y][1] = 0

    def get_prob(self, i, j):
        nature = 1
        urban = 1
        for k in range(3):
            for n in range(3):
                try:
                    if self.world.get_feature.type == 1:
                        nature += 1
                    elif self.world.get_feature.type == 2:
                        urban += 1
                except:
                    None
        return (nature / (urban + nature))

    def fill_world(self):
        for i in range(self.size):
            for j in range(self.size):
                nature_prob = self.get_prob(i, j)
                self.world[i][j][0] = Feature(nature_prob)

    
                    
                    
                    
                    
                
        
            

    def get_poet(self, x, y):
        return self.world[x][y][1]
    def get_feature(self, x, y):
        return self.world[x][y][0]




