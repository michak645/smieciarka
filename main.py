import collections
import math
import numpy
import pygame
import random
import sys

from astar import *
from garbage import *
from settings import *

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
        tasks.append(trash)

print('Today is: {}'.format(today))
print('Schedule: {}'.format(schedule[today]))
print('Tasks: {}'.format(len(tasks)))


def tasks_costs(tasks, start_x, start_y):
    tasks_paths = {}
    for task in tasks:
        trash_x = task['coordinates'][0]
        trash_y = task['coordinates'][1]
        task_path = AStar(
            start_x,
            start_y,
            direction,
            trash_x,
            trash_y,
            costs
        ).process()
        tasks_paths[len(task_path)] = task
    ordered_tasks_paths = collections.OrderedDict(sorted(tasks_paths.items()))
    return ordered_tasks_paths
    # return sorted(tasks_paths, key=lambda k: k['coordinates'])


ble = tasks_costs(tasks, math.floor(x / 40), math.floor(y / 40))
list(ble.items())[0]

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

    if path and moves < len(path):
        x = path[moves][0] * 40
        y = path[moves][1] * 40
        direction = path[moves][2]
        print(path[moves][2])
        moves += 1
    else:
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
                screen.blit(can, (col_i, row_i))
                bin_type_string = font.render(
                    trash_list[trash_coordinates]['trash_type'][:4].lower(),
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
