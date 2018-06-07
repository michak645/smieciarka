import pygame

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
