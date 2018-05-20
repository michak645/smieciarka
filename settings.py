import pygame

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 12)


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
    'colored_glass',
    'white_glass',
    'eco',
    'paper',
    'mixed',
    'large',
]

trash_fillings = [
    'empty',
    'half_full',
    'full',
]

# Can image
can = pygame.image.load('resources/can.png')
can = pygame.transform.scale(can, (car_width, car_height))

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
    'monday': [
        'mixed',
        'plastic',
    ],
    'tuesday': [
        'mixed',
        'colored_glass',
    ],
    'wednesday': [
        'mixed',
        'eco',
    ],
    'thursday': [
        'mixed',
        'paper',
        'plastic',
    ],
    'friday': [
        'large',
    ],
    'saturday': [
        'mixed',
        'white_glass',
    ],
    'sunday': [
        'mixed',
        'eco',
    ],
}
