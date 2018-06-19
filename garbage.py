import random

from settings import *
from astar import *


trash_list = {}
for row in range(10):
    for column in range(10):
        if obstacles[row][column] == 2:
            trash_list[(column, row)] = {
                'coordinates': (column, row),
                'trash_type': random.choice(trash_types),
                'filling': random.choice(trash_fillings),
                'plastic_label_type': random.choice(plastic),
                'municipal_label_type': random.choice(municipal),
                'glass_label_type': random.choice(glass),
                'paper_label_type': random.choice(paper),
            }
