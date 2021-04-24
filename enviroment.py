"""
Noah Gans
CSCI 3725
M6
4/24/21
This file is a representation of the world poets can move in. It is a 3d array of width by length both of which are 
set for ten. The 3d dimension is of size 2 and the first index holds the enviormental features and the second index
holds a 0 if there is no poet in that spot and the poet if it is in that spot. It has two methods to get a printable
version which are it's __str__ which prints the enviromental features and the second (printy) which prints it's poet
locations
"""

import random
from enviormental_feature import Feature

class World:
    def __init__(self, name):
        """
        A world has a name, a size, and the 3d array which holds all of the data
        """
        self.name = name
        self.size = 10
        self.world = [[[0 for z in range(2)] for x in range(self.size)] for y in range(self.size)] 
        
    def __str__(self):
        """
        Go through the array and add the elements to a string with new lines at each row. Only pull enviromental
        features
        """
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
        """
        Go through the array and add the elements to a string with new lines at each row. Only pull poet locations
        """
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
        """
        This is a wierd funtion becase it can do one thing or two. If trying to set a poet location on top of
        another poet, the funtion returns false. Otherwise, the location of the poet is set to the input cordinates
        and then the funtion returns true. 
        """
        if self.world[x][y][1] != 0:
            return False
        else:
            self.world[x][y][1] = poet
            return True

    def clear_loc(self, x, y):
        """ SImple funtion to set the value at the input corddiantes to 0 representing the poet has moved from this
        location
        """
        self.world[x][y][1] = 0

    def get_prob(self, i, j):
        """this is a funtion that gets the probability of a spot in the world being a cetain type. The probability
        is proportional to the number of types around it. So, if there are a lot of nature spots around a blank one 
        needing to be set, the blank one will be set at a higher chace to nature. This gives the map some sort of 
        grouping of types insted of random features everywhere. 
        """
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
        """
        This funtion goes through the world and fills it with enviromental features proportional to the number of 
        features around it already made. 

        """
        for i in range(self.size):
            for j in range(self.size):
                nature_prob = self.get_prob(i, j)
                self.world[i][j][0] = Feature(nature_prob)

    def get_poet(self, x, y):
        """
        returns the poet dimension for the given x and y vaules
        """
        return self.world[x][y][1]
    def get_feature(self, x, y):
        """"
        Returns the enviromental feature at the given x, y points
        """
        return self.world[x][y][0]




