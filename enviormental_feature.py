"""
Noah Gans
CSCI 3725
M6
4/24/21
This class represents a feature in the world. There are either urban or natural features. The features are read
from respective files and chosen randomly. A feature has a type 1 = nature and 2 = urban, and also and element
which includes the features name and all of it's possible attributes.  
"""

import random
class Feature:
    def __init__(self, naure_prob):
        """
        A probability is input, and this determines which type of feature is made. The feature is made by 
        chosing a type and reciving the elements of the feature from the respective file. 

        """
        prob = random.uniform(0,1)
        if  prob < naure_prob:
            self.type = 1
            self.element = self.read_file("nature")
        else:
            self.type = 2
            self.element = self.read_file("urban")


    def read_file(self, name):
        """
        This method reads either the urban or nature txt file choses a random number 0 and 5, the number of 
        elements in both files, and then gets a list of the name and all the elements of the feature selected.
        """
        filename = name + ".txt"
        f = open(filename, "r")
        lines = f.readlines()
        element = random.randint(1, 5)
        index_to_read = 0
        for i, line in enumerate(lines):
            if line[0] == str(element):
                index_to_read = i
                break
        element_list = []
        line = lines[index_to_read]
        index = index_to_read
        while line[0] != '\n':
            element_list.append(line[:-1])
            index_to_read += 1
            line = lines[index_to_read]
        return (element_list)
    
    def __str__(self):
        """
        String representation is the name of the element which is the first index of self.element with the first
        two chars cut off
        """
        return self.element[0][2:]
            
        
        

