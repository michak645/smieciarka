import math
import random

import numpy
import pygame
import sys

from astar import (
    AStar,
    obstacles
)


path = []
# 2 dimensional array for obstacles


pygame.init()

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 12)


width, height = 400, 400
screen = pygame.display.set_mode((width, height))

step = 40

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

building = pygame.image.load('resources/dom1.png')
building = pygame.transform.scale(building, (car_width, car_height))

# TODO: Add rotations of the truck
# Truck direction
directions = ['N', 'S', 'E', 'W']
direction = 'S'

# Can image
can = pygame.image.load('resources/can.png')
can = pygame.transform.scale(can, (car_width, car_height))

# Garbage image
garbage = pygame.image.load('resources/garbage.jpg')
garbage = pygame.transform.scale(garbage, (car_width, car_height))

# 2 dimensional array of 10x10 elements
board = numpy.arange(100).reshape(10, 10)

# define array of costs
costs = []
for row in range(10):
    costs.append([])
    for column in range(10):
        costs[row].append(random.randint(10, 50))


# def can_move_up(x, y):
#     if obstacles[int(y / step) - 1][int(x / step)] == 0:
#         return True
#     else:
#         return False


# def can_move_down(x, y):
#     y = int(y / step)
#     x = int(x / step)
#     if y + 1 >= 10:
#         return False
#     if obstacles[y + 1][x] == 0:
#         return True
#     else:
#         return False


# def can_move_left(x, y):
#     if obstacles[int(y / step)][int(x / step) - 1] == 0:
#         return True
#     else:
#         return False


# def can_move_right(x, y):
#     x = int(x / step)
#     y = int(y / step)
#     if x + 1 >= 10:
#         return False
#     if obstacles[y][x + 1] == 0:
#         return True
#     else:
#         return False


# garbageA_x = 2 * step
# garbageA_y = 7 * step

# garbageB_x = 5 * step
# garbageB_y = 5 * step

# garbageC_x = 6 * step
# garbageC_y = 9 * step

# Params for drawing
clock = pygame.time.Clock()
clear = 0
moves = 0

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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if moves < len(path) and path:
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
                screen.blit(building, (col_i, row_i))
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

    # pressed = pygame.key.get_pressed()
    #
    # if pressed[pygame.K_w]:
    #     if can_move_up(x, y):
    #         y -= step
    # if pressed[pygame.K_s]:
    #     if can_move_down(x, y):
    #         y += step
    # if pressed[pygame.K_a]:
    #     if can_move_left(x, y):
    #         x -= step
    # if pressed[pygame.K_d]:
    #     if can_move_right(x, y):
    #         x += step
    #
    # if y >= height - car_height:
    #     y = height - step
    # elif y < 0:
    #     y = 0
    # if x > width - car_w:
    #     x = width - car_w
    # elif x < 0:
    #     x = 0

    # screen.blit(can, (width - 40, height - 40))

    # if x == garbageA_x and y == garbageA_y:
    #     garbageA_x = width - step
    #     garbageA_y = height - step
    #     clear += 1
    # if x == garbageB_x and y == garbageB_y:
    #     garbageB_x = width - step
    #     garbageB_y = height - step
    #     clear += 1
    # if x == garbageC_x and y == garbageC_y:
    #     garbageC_x = width - step
    #     garbageC_y = height - step
    #     clear += 1

    # screen.blit(garbage, (garbageA_x, garbageA_y))
    # screen.blit(garbage, (garbageB_x, garbageB_y))
    # screen.blit(garbage, (garbageC_x, garbageC_y))

    # if clear == 3:
    #     screen.fill((0, 0, 0))
    #
