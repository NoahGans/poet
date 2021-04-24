"""
Noah Gans
CSCI 3725
M6
4/24/21
This file is all one class, Poem class. It handles all of the work with turning the expirences of the
poets in the world into first poem_structure, and then into strings. A poem sturutre structure is a list
of lists that represent lines. Creating it in this form and then translating to strings allowed for easy scoring.
There are three poems a poet can make 1) observation, 2) connection, and 3) reflection. Each of these types
of poems have diffrent funtions that make the poem_structure (connection has two methods becase of size), and 
observation and connection poems are translated into strings using the same write_line method. Reflection
poems however use write_reflection_line() to be translated. 
"""
import random
import re
import statistics
class Poem:
    def __init__(self, poet):
        """ A Poem has an assosiated poet and a dictionary for identifying word types."""
        self.poet = poet
        self.dictionary = {}
        self.make_dict()#fills the dictionary 
        
    def write_struture(self):
        """ This is method that writes a poem stucture. Of the three choices of pomes all three have equal chance
        of being written. This method calls the appropriate poem funtion and returns the poem structure it 
        returns. 
        """
        pome_type = random.randint(1, 3)
        if pome_type == 1:
            poem_structure = self.make_reflection_poem_structure()
        elif pome_type == 2:
            poem_structure = self.make_connection_pome()
        else:
            poem_structure = self.make_observation_poem_structure()
        return poem_structure
    
    def make_reflection_poem_structure(self):
        """
        This method deals with the creation of the poem structure of a reflection poem. Two 
        types of poems can be made. One a comentary on the most influental expirence in the poets
        life, and two comentary on the character attribute changed the most. First the history
        of the poet is gone through and the event that created the largest change in the poet is 
        saved with its index. Next, the most common character attribute that was changed
        is found, and its index is saved. I used a list to store the mode and did the calcualtion twice,
        because the mode funtion was returning some weird results. The mode list and the index of the 
        event that resulted in the most chage are passed to finalize_reflection_poem.
        """
        
        max_change = 0
        index = 0
        mode_list = []

        #finds max change expirenced by poet
        for i, element in enumerate(self.poet.self_history):
            if abs(element[2]) > abs(max_change):
                max_change = element[2]
                index = i

        #finds most changed attribute
        for count in range(2):
            attribute_list = []
            for element in self.poet.self_history:
                attribute_list.append(element[count])
            try:
                mode_list.append(statistics.mode(attribute_list))
            except:
                mode_list.append(random.randint(0, 19))
        return self.finalize_reflection_poem(index, mode_list)
    
    def finalize_reflection_poem(self, index, mode_list):
        """
        This funtion handles all of the poem_struture creation. First, the poet making the poem is added
        to the poem_struture, then a choice beteen most significant event(1) or most effected attribute(2) poem is
        made. If the first, the a list of 1 and the index of the most extreme evnt is added to the poem_struture.
        Then this poem structure is returned. If the second, then lists of all the incidences that changed the mode character
        attribute are added with 2's to the poem structure. A intro and a outro are added to the poem structure,
        and the poem structure is returned
        """
        poem_struture = []
        poem_struture.append([self.poet]) 
        poem_type = random.randint(1,2)

        if poem_type == 1: #most significant event
            poem_struture.append([1, index])
        elif poem_type == 2:
            count_1 = 0
            for element in self.poet.self_history:
                if element[1] == mode_list[1]:
                    count_1 += 1
                    poem_struture.append([2, element])
            poem_struture.insert(1,[2, [1, mode_list[1]]])#intro to the poem
            poem_struture.append([2, [2, mode_list[1]]])#outro to the poem
        return poem_struture       

    def make_observation_poem_structure(self):
        """ 
        Make observation poem is the most simple poem of the three. At the top sampl is just a collection of 
        random numbers to use to add varience to the poems. This funtion finds the most observed enviormental feature
        the poet saw. WIth this feature, discriptions are added which are a list of the feature and the observation.
        The poem structure is then returned. 
        """
        sampl = ran_floats = [random.uniform(1,10) for _ in range(len(self.poet.observations[best_key]))]
        best_key = None
        best = 0
        #find enviormental feature most observed
        for key in self.poet.observations.keys():
            if len(self.poet.observations[key]) > best:
                best_key = key
                best = len(self.poet.observations[key])     
        
        poem_struture = []
        #randomly assign the subject to the selected enviormental feature to the poem structure
        if sampl[0] < 5:
            poem_struture.append([best_key])

        #go through the attributes of the feature, and either assert the feature or not and then make a discription. 
        for count, attribute in enumerate(self.poet.observations[best_key]):
            if sampl[count] < 2:
                poem_struture.append([best_key]) #assertion
            poem_struture.append([best_key, attribute])#discription
            if count > sampl[count]:#randomly stop poem
                break
        return poem_struture

    def make_connection_pome(self):
        """
        Make connection poem is straight forward in theory but looks big and spooky. This method selects a 
        random element from the poets observations, and then finds another observed object that has the most
        simmilar observations to it. Basically all of the attributes of every feature is compared to the attributes
        of the goal feature, and the best match is saved. Then the goal feature, best match feature, list of matching
        words, and max size of lists of observations is passed to the next funtion to build the poem_struture. 

        """
        base_key = random.choice(list(self.poet.observations.keys()))
        base_values = self.poet.observations[base_key]
        best_key_match = None
        best_score = 0
        key_list = list(self.poet.observations.keys())
        key_list.remove(base_key)
        same_words_final = []
        #go through all observed things
        for keys in key_list:
            same_words = []
            simmilar_score = 0
            #go through the attributes observed
            for value in self.poet.observations[keys]:
                #go through all the attributes of the selected feature
                for goal_value in base_values:
                    if value == goal_value:# if there is a match
                        if value not in same_words:#if this match hasent been observed
                            same_words.append(value)#append the matching word to same words
                        simmilar_score += 1
            if simmilar_score > best_score: #update the best match
                same_words_final = same_words
                best_score = simmilar_score
                best_key_match = keys 
        max_length = max(len(base_values), len(self.poet.observations[best_key_match]))
        return self.make_connection_poem_structure(base_key, best_key_match, same_words_final, max_length)
                              
    def make_connection_poem_structure(self, base_key, best_key_match, same_words_final, max_length):
        """
        This funtion works a lot like make_observation_poem_structure. Basically it does what 
        make_observation_poem_structure does for the first base_feature, then adds a line to the poem struture
        that indicates the linking attrubutes, then discribes the best match feature. Finishes with an assertion
        of the base feature. 


        """
        sampl = ran_floats = [random.uniform(1,10) for _ in range(max_length)]
        poem_struture = []
        for count, attribute in enumerate(self.poet.observations[base_key]):
            if sampl[count] < 1:
                poem_struture.append([base_key]) #assertion
            poem_struture.append([base_key, attribute])#discription
            if count > sampl[count]:
                break 
        poem_struture.append([base_key, same_words_final, best_key_match])#linking line. 
        for count, attribute in enumerate(self.poet.observations[best_key_match]):
            if sampl[count] < 1:
                poem_struture.append([best_key_match]) #assertion
            poem_struture.append([best_key_match, attribute])#discription
            if count > sampl[count]:
                break 
        
        poem_struture.append([base_key])#base feature assertion
        return poem_struture
        
    def write(self, poem_struture, style):
        """
        write calls the appropriate write line funtion for the given poem type given a flag. The returned line is
        added to the poem and a new line is added before the next line is made. The poem is then returned.
        """
        poem = ""
        for line in poem_struture:
            if style == -1:
                poem += self.write_line(line)
            else:
                poem += self.write_reflection_line(line)
            poem += "\n"
        return poem
       
    def write_line(self, line):
        """Both write line funtions are very long and deal with the translation of the poem structure into the
        poem string. They probably exceed what is stylistically good. With observation and connection poems
        there are three different lengths of lines from the poem_structure 1,2,3.
        If it is len(1) then it is an assertion and the code makes and assertion about the element in that line

        If it is len(2) then it is a discription. The code looks up what type of attribute the word is, selects the 
        apprpriate conjuntion, and combines it with the feature it is discribing.

        If it is len(3) then both features of the line are compared to a shared attribute and the appropriate conjuntion
        is selected

        The line is returned at the end
        """
        sampl = ran_floats = [random.uniform(1,10) for _ in range(10)]
        final_line = ""
        if len(line) == 1:
            start = random.choice(["There is a ", "A "])
            final_line = start + line[0]
        elif len(line) == 2:
            start = random.choice(["The " + line[0], "It"])
            word_type = self.get_word_type(line[1])
            if word_type == "n":
                final_line = start + " has " + line[1]
            elif word_type == "v":
                final_line = start + " " + line[1]
            elif word_type == "adj":
                final_line = start + " is " + line[1] 
            else:
                final_line = line[1] + " " + start
        elif len(line) == 3:
            for i in range(len(line[1])):
                start = random.choice(["The "])
                word_type = self.get_word_type(line[1][i])
                final_line = line[0] + " and " + line[2] + " both"
                if word_type == "n":
                    final_line += "have " + line[1][i]
                elif word_type == "v":
                    final_line +=  " " + line[1][i]
                elif word_type == "adj":
                    final_line += " are " + line[1][i] 
                else:
                    final_line += line[2][i] 
            final_line = start + final_line
        return final_line

    def write_reflection_line(self, line):
        sampl = ran_floats = [random.uniform(1,10) for _ in range(10)]
        final_line = ""
        if len(line) == 1:
            start = random.choice(["I am ", "My name is ", "Im "])
            final_line = start + line[0].name
            if sampl[0] < 5:
                final_line += "\n" + random.choice(["My life has been long"])
        else:
            final_line = self.write_reflection_line_helper(line)
        return final_line

    def write_reflection_line_helper(self, line):
        """
        Breaks down line writing to two funtions. The poem is either a most_impactful_element or a most_impacted_attribute
        poem. This is  
        """
        if line[0] == 1:
            return self.write_most_impactful_element_line(line)
        else:
            return self.write_most_impacted_attribute_line(line)
        
    def write_most_impactful_element_line(self, line):
        """
        This method writes a line for most impactful element poem. It adds to the line appropriate intduction if
        it is a poet or a feature that created the largest change. Then the attribute effected is added. Following
        this wheater or not it was an increase or decrease in the respective atribute determines what is said about
        it. If it was a decease then there is a chance that the lines discribing features that helped increase the 
        respective character trait are added. 
        """
        sampl = ran_floats = [random.uniform(1,10) for _ in range(10)]
        final_line = ""
        if type(self.poet.self_history[line[1]][0]) != type(self.poet):
            final_line += "A " + self.poet.self_history[line[1]][0]#if feature just saw "A"
        else:
            final_line += self.poet.self_history[line[1]][0].name #if poet use name
        final_line += " had the largest influnce on me \n"
        final_line += "My " + self.poet.attributes[self.poet.self_history[line[1]][1]] #introduce attribute effected
        
        if (self.poet.self_history[line[1]][2]) < 0:#negative shift
            try:
                final_line += " declined after interacting with " + self.poet.self_history[line[1]][0].name + "\n"
            except:
                final_line += " declined after interacting with a " + self.poet.self_history[line[1]][0] + "\n"

            if sampl[1] < 9:#talk about what helped
                final_line += "however \n"
                for element in self.poet.self_history:
                    if element[1] == self.poet.self_history[line[1]][1] and element[2] > 0:
                        final_line += "A " + element[0] + " helped my " + self.poet.attributes[self.poet.self_history[line[1]][1]] + "\n"
        else:#positive shift
            try:
                final_line += random.choice([" increased after interacting with " + self.poet.self_history[line[1]][0].name, " increased from them"]) + "\n"
            except:
                final_line += random.choice([" increased after interacting with a " + self.poet.self_history[line[1]][0], " increased from it"]) + "\n"
        return final_line

    def write_most_impacted_attribute_line(self, line):
        """
        This method writes about all the things that effected a specific attribute of a poet. The first conditional
        is only false for the into and outro added, so it creates most of the writing. The fist conditional
        writes about how the feature or poet impacted their respective character attribute. It is codded to 
        acount for positve and negative influence. The other two possibilities are the intro which writes 
        "My state of ..." and the outro which highlights the final state of that poets character attribute.


        """
        final_line = ""
        if type(line[1][0]) != int:
            if line[1][2] > 0:
                try:
                    final_line += "The " + line[1][0] + random.choice([" gave ", " helped my ", " instilled "]) +  self.poet.attributes[line[1][1]]
                except:
                    final_line += line[1][0].name + random.choice([" gave ", " helped my ", " instilled "]) +  self.poet.attributes[line[1][1]]

            else:
                try:
                    final_line += "The " + line[1][0] + random.choice([" reduced my ", " hurt my ", " destroyed my "]) +  self.poet.attributes[line[1][1]]
                except:
                    final_line += line[1][0].name + random.choice([" reduced my ", " hurt my ", " destroyed my "]) +  self.poet.attributes[line[1][1]]                            
        elif line[1][0] == 1:
            final_line += "My state of " + self.poet.attributes[line[1][1]] 
        else:
            if self.poet.character_list[line[1][1]] > .5:
                final_line += "I have become " + self.poet.attributes[line[1][1]]
            else:
                final_line += "This left me without " + self.poet.attributes[line[1][1]]
        return final_line     
       
    def get_word_type(self, word):
        """This class returns the type of a word given a word. It searches through the dict to find the word,
        and returns its type. If no word is found then adj is returned. 
        """ 
        try:   
            return self.dictionary[word][0]
        except:
            return("adj")

    def make_dict(self):
        """
        This funtion reads a txt dictonary and makes a python dictionary with the keys being the 
        lowercase words and the values being a tuple of type and definition
        """
        file1 = open('dict.txt', 'r')
        Lines = file1.readlines()
        listofstuff = []
        count = 0
        for line in Lines:
            if len(line) > 5:
                try:
                    word = ""
                    word_type = ""
                    definition = []
                    word_uncut = re.findall(".*  ", line)[0]
                    word = word_uncut[:-2]
                    value = len(word_uncut)
                    typey = re.findall( "  .*?\.", line)[0]
                    if "v" in typey or "past" in typey:
                        word_type = "v"
                    elif "adj" in typey:
                        word_type = "adj"
                    else:
                        word_type = "n"
                    first_def = re.findall("[A-Z][a-z ].*?\.",line[value:])
                    second_def = re.findall("[1-9].*?\.", line[value:])
                    for definition in second_def:
                        first_def.append(definition[1:])
                    definition = first_def
                    self.dictionary.update({word.lower() : (word_type, definition)})
                except:
                    count += 1

       
        
            
          
         
            
            


    




                
        
            

        

        






