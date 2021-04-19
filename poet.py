import random
from enviroment import World
from poem_maker import Poem
class Poet:
  def __init__(self, name, world):
    self.world = world
    self.name = name
    self.character_list = []
    for i in range(19):
      self.character_list.append(random.uniform(0,1))
    self.x_location = random.randint(0, world.size - 1)
    self.y_location = random.randint(0, world.size - 1)
    self.observations = {}
    self.interactions = []
    self.enviormental_history = []
    self.social_history = []
    self.self_history = []
      
  def __str__(self):
    return self.name

  def move(self):
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
    
    if self.world.set_poet_loc(temp_x, temp_y, self):
      self.world.clear_loc(self.x_location, self.y_location)
      self.x_location = temp_x
      self.y_location = temp_y
      return (-1, 0)
    else:
      return(temp_x, temp_y)
  
  def observe(self):
    current_feature = self.world.get_feature(self.x_location, self.y_location)
    self.enviormental_history.append(str(current_feature.type) + " " + current_feature.element[0][2:])
   
    if current_feature.element[0][2:] not in self.observations.keys():
      self.observations.update({current_feature.element[0][2:]: [ random.choice(current_feature.element[1:] )]})
    else:
      self.observations.get(current_feature.element[0][2:]).append(random.choice(current_feature.element[1:]))

  def reflect(self):
    current_feature = self.world.get_feature(self.x_location, self.y_location)
    index = random.randint(0,18)
    trait = self.character_list[index]
    change_value = random.uniform(0,1)
    change = trait - ((trait + change_value) / 2)
    self.character_list[index] = (trait + change_value) / 2
    self.self_history.append((current_feature, change))

      
  
  def act(self):
    self.observe()
    self.reflect()


  def interact(self, poet):
    sum = 0
    for i in range(len(self.character_list)):
      if abs(self.character_list[i] - poet.character_list[i]) > .5:
        change_value = poet.character_list[i]
        change_dir = self.character_list[i] - poet.character_list[i]
        self.character_list[i] = (self.character_list[i] + change_value) / 2
        self.self_history.append((poet, change_dir))
    
    


  def write(self):
    pome = Poem(self)






  def expirence(self):
    selection_num = radom.randint(0, len(self.observations))



  
  

    
    



def run(iterations, population):
  for i in range(iterations):
    for poet in population:
      moved_poet = poet.move()
      if moved_poet[0] < 0:
        poet.act()
      else:
        poet.interact(poet.world.get_poet(moved_poet[0], moved_poet[1]))

  print(world.printy())
      
      
  

  

world = World("cow")

world.fill_world()
print(world)
john = Poet("john", world)
bob = Poet("bob", world)
bob1 = Poet("bob1", world)
bob2 = Poet("bob2", world)
bob3 = Poet("bob3", world)
pop = [john, bob, bob1, bob2, bob3]

run(100, pop)

print(pop[0].observations)
pop[0].write()




# Red: Passion, Love, Anger.
# Orange: Energy, Happiness, Vitality.
# Yellow: Happiness, Hope, Deceit.
# Green: New Beginnings, Abundance, Nature.
# Blue: Calm, Responsible, Sadness.
# Purple: Creativity, Royalty, Wealth.
# Black: Mystery, Elegance, Evil.
# Gray: Resurved, Conservative, Formality