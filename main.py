import math
import numpy
import pydotplus
import pygame
import random
import sys

from sklearn.externals.six import StringIO
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz

from astar import *
from garbage import *
from settings import *
from tree import table, results


path = []

pygame.init()

# 2 dimensional array of 10x10 elements
board = numpy.arange(100).reshape(10, 10)

# define array of costs
costs = []
for row in range(10):
    costs.append([])
    for column in range(10):
        costs[row].append(random.randint(10, 50))

# Params for drawing
clock = pygame.time.Clock()
clear = 0
moves = 0
moves2 = 0

# today is
today = random.choice(days)
today_schedule = schedule[today]

tasks = []
for coords, trash in trash_list.items():
    if trash['trash_type'] in today_schedule:
        trash['collected'] = False
        tasks.append(trash)

print(tasks[0])

print('Today is: {}'.format(today))
print('Schedule: {}'.format(schedule[today]))
print('Tasks: {}'.format(len(tasks)))


v = DictVectorizer(sparse=False)
v.fit_transform(table)
X = v.fit_transform(table)
Y = results
dt = DecisionTreeClassifier()
dt.fit(X, Y)


dot_data = StringIO()
export_graphviz(
    dt,
    out_file=dot_data,
    feature_names=v.get_feature_names(),
    filled=True,
    rounded=True,
    impurity=False,
)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf('decision_tree.pdf')


def increase_capacity(x, y):
    global truck_capacity
    x = math.floor(x / 40)
    y = math.floor(y / 40)
    trash_coordinates = (x, y)
    trash = trash_list.get(trash_coordinates)
    if trash:
        check = {
            'filling': trash['filling'],
            'day': today,
            'type': trash['trash_type'],
            'truck_filling': capacity
        }
        if dt.predict(v.transform(check)) and not trash['collected']:
            if trash['filling'] == 'half':
                truck_capacity += 1
            elif trash['filling'] == 'full':
                truck_capacity += 2
            print('capacity: {}/{}'.format(truck_capacity, max_capacity))
            trash['collected'] = True
            trash['filling'] = 'empty'


# building_choices = [building1, building2, building3]
# building = random.choice(building_choices)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            goal_x = math.floor(pos[0] / 40)
            goal_y = math.floor(pos[1] / 40)
            print(
                'start: {},{}'.format(
                    math.floor(x / 40),
                    math.floor(y / 40)
                )
            )
            print('goal: {},{}'.format(goal_x, goal_y))
            path = AStar(
                math.floor(x / 40),
                math.floor(y / 40),
                direction,
                goal_x,
                goal_y,
                costs
            ).process()
            print('Path: {}'.format(path))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if truck_capacity == 0:
        capacity = 'empty'
    elif truck_capacity > 0 and truck_capacity < 7:
        capacity = 'half'
    elif truck_capacity >= 7:
        capacity = 'full'

    if tasks and moves == 0:
        if truck_capacity >= max_capacity - 1:
            print('capacity: {}/{}'.format(truck_capacity, max_capacity))
            print('Max capacity of truck reached')
            print('Going back to start point to get rid of trashes')
            path = AStar(
                math.floor(x / 40),
                math.floor(y / 40),
                direction,
                0,
                0,
                costs
            ).process()
            truck_capacity = 0
        else:
            trash = tasks[0]
            trash_x, trash_y = trash['coordinates']
            path = AStar(
                math.floor(x / 40),
                math.floor(y / 40),
                direction,
                trash_x,
                trash_y,
                costs
            ).process()
            tasks.remove(trash)

    if path and moves < len(path):
        x = path[moves][0] * 40
        y = path[moves][1] * 40
        direction = path[moves][2]
        # wyświetlanie ścieżki
        # print(path[moves][2])
        # truck_fuel -= 1
        moves += 1
    else:
        increase_capacity(x, y)
        moves = 0
        path = []

    row_i = 0
    col_i = 0
    for row in obstacles:
        for cell in row:
            if cell == 1:
                pygame.draw.rect(screen, (255, 255, 255),
                                 (col_i, row_i, step, step))

                screen.blit(building2, (col_i, row_i))
            elif cell == 2:
                # cell is trash
                trash_coordinates = (
                    math.ceil(col_i / 40),
                    math.ceil(row_i / 40)
                )
                check = {
                    'filling': trash_list[trash_coordinates]['filling'],
                    'day': today,
                    'type': trash_list[trash_coordinates]['trash_type'],
                    'truck_filling': 'empty'
                }
                if check['type'] in schedule[today]:
                    if check['filling'] == 'empty':
                        screen.blit(can_yellow, (col_i, row_i))
                    else:
                        screen.blit(can_green, (col_i, row_i))
                else:
                    screen.blit(can_red, (col_i, row_i))
                bin_type_string = font.render(
                    '{}-{}'.format(
                        trash_list[trash_coordinates]['trash_type'][:2].upper(),
                        trash_list[trash_coordinates]['filling'][:1].upper()
                    ),
                    False,
                    (0, 0, 0)
                )
                screen.blit(bin_type_string, (col_i, row_i))
                pass
            else:
                cost = font.render(
                    str(costs[int(row_i / 40)][int(col_i / 40)]),
                    False,
                    (255, 255, 255)
                )
                screen.blit(cost, (col_i, row_i))
            col_i += step
            if col_i == width:
                col_i = 0
        row_i += step
        if row_i == height:
            row_i = 0

    if direction == 'N':
        screen.blit(car_n, (x, y))
    elif direction == 'S':
        screen.blit(car_s, (x, y))
    elif direction == 'E':
        screen.blit(car_e, (x, y))
    elif direction == 'W':
        screen.blit(car_w, (x, y))

    pygame.display.flip()
    screen.fill((169, 169, 169))
    clock.tick(5)
