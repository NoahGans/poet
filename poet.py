"""
Noah Gans
CSCI 3725
M6
4/24/21
This file is the driver for the whole program. It contains the Poet class and a few other funtions to aid in the 
scoring and choosing of a final poem. The Poet class is a representation of a poet. A Poet first expirnces the 
world by moving around and taking a few actions, and eventually moves on to writing poetry using the Poem class. 
A Poet has many attributes, that hold its location in the world, what its seen and its inital conditions/attributes.
Each poet has 19 attributes that are set at the bigning of their lives. These will change throughout their time,
and will usually end up in their writing.
"""

import random
from enviroment import World
from poem_maker import Poem
import os

class Poet:
  def __init__(self, name, world):
    """
    This initializes all the attributes of a poet. It takes a world for the poet to live in and a name of the poet.
    """
    self.world = world
    self.name = name
    self.character_list = [] #holds values for respective attributes below
    self.attributes = ["Generosity", "Integrity", "Loyalty", "Devotion", "Loving", "Kindness", "Sincerity", "Self-control", "Peacefulness", "Faithfulness", "Patience", "Determination", "Persistence", "Adventurous", "Fairness", "Cooperation", "Tolerance", "Optimism", "Spirituality"]
    for i in range(19):#fill character list
      self.character_list.append(random.uniform(0,1))
    self.x_location = random.randint(0, world.size - 1) # A random starting location is chosen
    self.y_location = random.randint(0, world.size - 1)
    self.observations = {}#this holds what they observe from what they see
    self.interactions = []#this holds the history of who the poet interacted with
    self.enviormental_history = []#this holds the history of what enviormental features the poet saw
    self.self_history = []#This holds change in self from enviorment

  def __str__(self):
    """ The string representation of a Poet is their name"""
    return self.name

  def move(self):
    """ This funtion moves a poet on the board to their next location. A Poet can either move up, down, left, or right.
    The funtion will continue to loop until it finds a place to move that is valid(within the borders of the world).
    After finding a valid moving spot, it then checks if their is a poet in the spot it plans to move to. If not,
    the poet moves to that spot and its location is updated. if there is a poet in that spot, than the funtion 
    returns the location it was going to move to the poet planning to move knows what poet it interacted with. The
    poet planning to move stays in the same location if it hits another poet.
    """
    moved = False
    while(not moved):
      temp_x = self.x_location
      temp_y = self.y_location
      dir = random.randint(1, 4)
      if dir == 1:
        temp_x += 1
      elif dir == 2:
        temp_y += 1
      elif dir == 3:
        temp_x -= 1
      else:
        temp_y -= 1
      if not (temp_y > 9 or temp_y < 0 or temp_x > 9 or temp_x < 0):
        moved = True
    
    # no poet conflict. world.set_poet_loc sets new location if no conflict
    if self.world.set_poet_loc(temp_x, temp_y, self):
      self.world.clear_loc(self.x_location, self.y_location)
      self.x_location = temp_x
      self.y_location = temp_y
      return (-1, 0)
    else:
    #ran into another poet, return the other poet's location
      return(temp_x, temp_y)
  
  def observe(self):
    """
    Observe is one of the two actions that is taken by a poet when entering a space a new space. With observe,
    the poet observes the current feature in the area he, she, or they is in. This feature is added to the poet's
    enviromental history. The poet then adds the feature to their observations if it is not already in it, and then
    chooses a attribute of the feature randomly to observe. THe observation dictionary is then a key of the feature 
    name, and a value of a list of all observed attributes of that feature. 
    """
    current_feature = self.world.get_feature(self.x_location, self.y_location)
    self.enviormental_history.append(current_feature.element[0][2:])
   
    if current_feature.element[0][2:] not in self.observations.keys():
      self.observations.update({current_feature.element[0][2:]: [random.choice(current_feature.element[1:])]})
    else:
      self.observations.get(current_feature.element[0][2:]).append(random.choice(current_feature.element[1:]))

  def reflect(self):
    """
    Reflect is taken when the poet enters a space not ocupied by another poet. After observing the enviromental feature
    the poet then reflects on that feature. This is the process of having the enviromental feature change a attribute
    of the poet. First the feature is found, then one of the inital 19 attributes is randomly selected to be changed.
    A random 0-1 float is generated, and avraged with the current value of the selected attribute to create a change
    in that specific attribute. The avrage is set, and the feature, attribute changed(index), and amount changed by 
    are saved to the self history. By observing the self history, an understanding of how the poet was personally 
    effected from the world can be determined.  
    """
    current_feature = self.world.get_feature(self.x_location, self.y_location)
    index = random.randint(0,18)
    trait = self.character_list[index]
    change_value = random.uniform(0,1)
    change = ((trait + change_value) / 2) - trait
    self.character_list[index] = (trait + change_value) / 2
    self.self_history.append([current_feature.element[0][2:], index, change])

  def act(self):
    """
    Act first calls the observe method and then the reflect method. It is called when the poet did not run into
    another poet when moving.

    """
    self.observe()
    self.reflect()



  def interact(self, poet):
    """
    Interact is simmilar to reflect in that it effects the poets self_history. Interact basically finds any 
    large diffrence(>.5) between the two poets character attributes. If there is a large diffrence, the poet 
    who ran into the other has their respective character attribute reset to the avrage of the two poets. Then, 
    like reflect, the poet who was met, the attribute changed(i), and the magnitude of that change are saved in
    the interacting poet's self history. Interact is one way. It is taken when one poet moves into a spot with another
    poet. 
    """
    sum = 0
    self.interactions.append(poet)
    for i in range(len(self.character_list)):
      if abs(self.character_list[i] - poet.character_list[i]) > .5:
        change_value = poet.character_list[i]
        change_dir = poet.character_list[i] - self.character_list[i] 
        self.character_list[i] = (self.character_list[i] + poet.character_list[i]) / 2
        self.self_history.append([poet, i, change_dir])


  def make_pome(self):
    """
    Make poem creates a Poem class, and returns a poem struture from the Poem class. 
    """
    pome = Poem(self)
    return pome.write_struture()


def score_poem(poem_structure, population):
    """
    Score Poem is a method to score a poem. Like in society we value poems that speak to us the most. We want pomes
    that are relatable and provide a comentary on a life that we relate to. Score_poem achives this but with the
    society created in this program. A score is proportional to the amount of content in the poem that others
    in the society have also expirenced. To do this, the funtion goes through each poem and if the content of that
    poem is shared by the history of other poets in the population, the poems score is increased. Pomes recive many
    more points if two multiple poets share the same poet interaction becase this occurance is more rare.   
    """
    score = 0
    for element in poem_structure:
      for poet in population:
        try:
          if element[0] in poet.enviormental_history or element[1] in poet.enviormental_history:
            score += 1
        except:
          None
        try:
          if element[1][0] in poet.enviormental_history:
            score += 1
        except:
          None
        try:
          if element[1][0] in population:
            score +=  30
        except:
          None
    if len(poem_structure) == 2:
      score += 40
    return score
    



def run(iterations, population):
  """
  Run is the driver for the first part of this program, the simulation. It funtions by moving poets around the
  world. If the poet can move, then it is in a new space and therfore act(). If the poet hits another poet,
  then the poet interacts with the one it ran into.  Run takes in iteration which is the represents the number
  of moves each poet makes in the simulation.

  """
  for i in range(iterations):
    for poet in population:
      moved_poet = poet.move()
      if moved_poet[0] < 0:
        poet.act()
      else:
        poet.interact(poet.world.get_poet(moved_poet[0], moved_poet[1]))
  

   
def create_pomes(population, num):
  """
  Create poems makes a list of pome strutures. It takes in a population and a num which will represent the 
  number of poems made from each poet. This method funtions by going through all the poets and then through the 
  num given and each time the poet atempts to make a poem. This poem is then added to the final list of pomes 
  which is returned. This population of pomes is then scored and the best is presented.  
  """
  list_of_pomes = []
  count = 0
  total = num * len(pop)
  for poet in population:
    for x in range(num):
      count += 1
      print(str((count / total) * 100) + "% of the way done writing poetry")
      try:
        poem = poet.make_pome()
        list_of_pomes.append((poem, poet))
      except:
        None
  return list_of_pomes

def get_best_poem(poems):
  """
  A simple method that employs the socre_poem() method to return the best pome of the set of all poems produced. 
  """
  max = 0
  best_poem = None
  for poem in pomes:
    if score_poem(poem[0], pop) > max:
      max = score_poem(poem[0], pop)
      best_poem = poem
  return best_poem



def get_style(poem):
  """
  Becase there are two different styles, this method gets the style of the poem. This is esily done, becase
  all reflection poems have ints in them, and the flag for a reflection pome is >0. So, if there is an int in the poem structure
  than it is a reflection poem. Otherwise it's not and gets a -1 flag
  """
  style = 0
  for item in poem:
    for part in item:
      if type(part) == int:
        style = 1
        return style
  style = -1
  return style

if __name__ == "__main__":
  """
  Main method. Creates a population of 5, runs the simulation 100 times, makes pomes, scores and gets the
  best poem writes the poem fromt the poem structure, then speaks each line of the poem. 
  """
  world = World("world")
  world.fill_world()
  print(world)
  john = Poet("john", world)
  bob = Poet("Lauren", world)
  bob1 = Poet("Kevin", world)
  bob2 = Poet("Sarah", world)
  bob3 = Poet("Jan", world)
  pop = [john, bob, bob1, bob2, bob3]
  run(100, pop)

  pomes = create_pomes(pop, 5)
  best_poem = get_best_poem(pomes)
  style = get_style(best_poem[0])
  pome_write = Poem(best_poem[1])
  poem = (pome_write.write(best_poem[0], style))
  poem_list = poem.split('\n')
  for line in poem_list:
    os.system("say " + line)














