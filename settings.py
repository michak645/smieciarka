import pygame
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 16)


width, height = 400, 400
screen = pygame.display.set_mode((width, height))

step = 40

# TRUCK SETTINGS

# garbage truck params
# truck location x and y
x = 0
y = 0
# height and width of the truck
car_width = 40
car_height = 40
# Truck image
# car = pygame.image.load('resources/car.png')
# car = pygame.transform.scale(car, (car_width, car_height))


car_n = pygame.image.load('resources/car_n.png')
car_s = pygame.image.load('resources/car_s.png')
car_e = pygame.image.load('resources/car_e.png')
car_w = pygame.image.load('resources/car_w.png')

car_s = pygame.transform.scale(car_s, (car_width, car_height))
car_n = pygame.transform.scale(car_n, (car_width, car_height))
car_e = pygame.transform.scale(car_e, (car_width, car_height))
car_w = pygame.transform.scale(car_w, (car_width, car_height))

global truck_capacity
global truck_fuel
global max_capacity
truck_fuel = 30
truck_capacity = 0
max_capacity = 8

capacity_options = []
for cap in range(20):
    capacity_options.append(cap + 1)

# Truck direction
global direction
direction = 'S'

# BUILDING SETTINGS

# building1 = pygame.image.load('resources/building01.png')
building2 = pygame.image.load('resources/building02.png')
# building3 = pygame.image.load('resources/building03.png')

# building1 = pygame.transform.scale(building1, (car_width, car_height))
building2 = pygame.transform.scale(building2, (car_width, car_height))
# building3 = pygame.transform.scale(building3, (car_width, car_height))


# TRASH SETTINGS

# plastiki, szkło białe, szkło kolorowe, zielone, papier, mieszane, gabaryty
# dzień wywożenia śmieci - każdy typ w osobne dni
# czy kontener ze śmieciami jest pełny czy pusty

trash_types = [
    'plastic',
    'glass',
    'municipal',
    'paper',
]

trash_fillings = [
    'empty',
    'half',
    'full',
]

# Can image
can = pygame.image.load('resources/can.png')
can = pygame.transform.scale(can, (car_width, car_height))

can_red = pygame.image.load('resources/can_red.png')
can_red = pygame.transform.scale(can_red, (car_width, car_height))

can_green = pygame.image.load('resources/can_green.png')
can_green = pygame.transform.scale(can_green, (car_width, car_height))

can_yellow = pygame.image.load('resources/can_yellow.png')
can_yellow = pygame.transform.scale(can_yellow, (car_width, car_height))

# Garbage image
garbage = pygame.image.load('resources/garbage.jpg')
garbage = pygame.transform.scale(garbage, (car_width, car_height))

# Types image

w, h = 2, 4;
plastic = [[0 for x in range(w)] for y in range(h)]

w, h = 2, 4;
municipal = [[0 for x in range(w)] for y in range(h)]

w, h = 2, 4;
glass = [[0 for x in range(w)] for y in range(h)]

w, h = 2, 4;
paper = [[0 for x in range(w)] for y in range(h)]

for x in range(4):
  plastic1 = pygame.image.load('resources/plastic'+str(x+1)+'.png')
  plastic1 = pygame.transform.scale(plastic1, (car_width, car_height))
  plastica1 = image.load_img('resources/plastic'+str(x+1)+'.png', target_size = (64, 64), grayscale=True)
  plastic[x][0] = plastic1
  plastic[x][1] = plastica1
for x in range(4):
  glass1 = pygame.image.load('resources/glass'+str(x+1)+'.png')
  glass1 = pygame.transform.scale(glass1, (car_width, car_height))
  glassa1 = image.load_img('resources/glass'+str(x+1)+'.png', target_size = (64, 64), grayscale=True)
  glass[x][0] = glass1
  glass[x][1] = glassa1
for x in range(4):
  municipal1 = pygame.image.load('resources/municipal'+str(x+1)+'.png')
  municipal1 = pygame.transform.scale(municipal1, (car_width, car_height))
  municipala1 = image.load_img('resources/municipal'+str(x+1)+'.png', target_size = (64, 64), grayscale=True)
  municipal[x][0] = municipal1
  municipal[x][1] = municipala1
for x in range(4):
  paper1 = pygame.image.load('resources/paper'+str(x+1)+'.png')
  paper1 = pygame.transform.scale(paper1, (car_width, car_height))
  papera1 = image.load_img('resources/paper'+str(x+1)+'.png', target_size = (64, 64), grayscale=True)
  paper[x][0] = paper1
  paper[x][1] = papera1

# days list
days = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',
]


schedule = {
    'monday': ['glass', 'municipal', ],
    'tuesday': ['municipal', 'plastic', ],
    'wednesday': ['paper', 'glass', ],
    'thursday': ['plastic', 'glass', ],
    'friday': ['glass', 'municipal'],
    'saturday': ['paper', 'plastic'],
    'sunday': ['glass', ],
}
