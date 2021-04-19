import random

class Feature:
    def __init__(self, naure_prob):
        prob = random.uniform(0,1)
        if  prob < naure_prob:
            self.type = 1
            self.element = self.read_file("nature")
        else:
            self.type = 2
            self.element = self.read_file("urban")


    def read_file(self, name):
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
        return self.element[0][2:]
            
        
        

