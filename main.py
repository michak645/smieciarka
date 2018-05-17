import math
import random

import numpy
import pygame
import sys
import time


path = []
# 2 dimensional array for obstacles
obstacles = numpy.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
])

# define A*
class Node(object):
    def __init__(self, x, y, cost):
        """
        Initialize new cell
        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = cost


class AStar(object):
    def __init__(self, startx, starty, endx, endy, costs):
        self.opened = []
        self.closed = []
        self.cells = []
        for y in range(10):
            self.cells.append([])
            for x in range(10):
                self.cells[y].append(
                    Node(x, y, costs[y][x])
                )
        self.start = self.get_cell(startx, starty)
        self.end = self.get_cell(endx, endy)

    def get_heuristic(self, cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def get_cell(self, x, y):
        return self.cells[y][x]

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x > 0 and obstacles[cell.y][cell.x - 1] == 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.x < 9 and obstacles[cell.y][cell.x + 1] == 0:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0 and obstacles[cell.y - 1][cell.x] == 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.y < 9 and obstacles[cell.y + 1][cell.x] == 0:
            cells.append(self.get_cell(cell.x, cell.y + 1))

        return cells

    def display_path(self):
        cell = self.end

        path = []
        while cell is not self.start:
            path.append((cell.x, cell.y))
            cell = cell.parent
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        adj.g = cell.g + adj.cost
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        for y in range(10):
            for x in range(10):
                self.cells[y][x].h = self.get_heuristic(self.cells[y][x])

        cell = self.start

        self.opened.append((cell.f, cell))

        while len(self.opened):
            self.opened.sort(key=lambda tup: tup[0])
            key, cell = self.opened.pop(0)
            self.closed.append(cell)

            if cell == self.end:
                print('path: ')
                print(self.display_path())
                return self.display_path()

            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.g == 0:
                    adj_cell.g = adj_cell.cost + cell.g
                    adj_cell.parent = cell
                adj_cell.f = adj_cell.g + adj_cell.h
                if adj_cell not in self.closed:
                    self.opened.append((adj_cell.f, adj_cell))




pygame.init()

pygame.font.init()
success = pygame.font.SysFont('Comic Sans MS', 12)


width, height = 400, 400
screen = pygame.display.set_mode((width, height))

step = 40

# garbage truck params
# truck location x and y
x = 0
y = 0
# height and width of the truck
car_w = 40
car_h = 40
# Truck image
car = pygame.image.load('resources/car.png')
car = pygame.transform.scale(car, (car_w, car_h))

building = pygame.image.load('resources/dom1.png')
building = pygame.transform.scale(building, (car_w, car_h))

# TODO: Add rotations of the truck
# Truck direction
directions = ['N', 'S', 'E', 'W']
direction = "S"

# Can image
can = pygame.image.load('resources/can.png')
can = pygame.transform.scale(can, (car_w, car_h))

# Garbage image
garbage = pygame.image.load('resources/garbage.jpg')
garbage = pygame.transform.scale(garbage, (car_w, car_h))

# 2 dimensional array of 10x10 elements
board = numpy.arange(100).reshape(10, 10)

# define array of costs
costs = []
for row in range(10):
    costs.append([])
    for column in range(10):
        costs[row].append(random.randint(10, 50))


def can_move_up(x, y):
    if obstacles[int(y/step)-1][int(x/step)] == 0:
        return True
    else:
        return False


def can_move_down(x, y):
    y = int(y / step)
    x = int(x / step)
    if y+1 >= 10:
        return False
    if obstacles[y + 1][x] == 0:
        return True
    else:
        return False


def can_move_left(x, y):
    if obstacles[int(y/step)][int(x/step)-1] == 0:
        return True
    else:
        return False


def can_move_right(x, y):
    x = int(x/step)
    y = int(y/step)
    if x+1 >= 10:
        return False
    if obstacles[y][x+1] == 0:
        return True
    else:
        return False


garbageA_x = 2 * step
garbageA_y = 7 * step

garbageB_x = 5 * step
garbageB_y = 5 * step

garbageC_x = 6 * step
garbageC_y = 9 * step

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
            goal_x = math.floor(pos[0]/40)
            goal_y = math.floor(pos[1]/40)
            print('start: {},{}'.format(math.floor(x / 40), math.floor(y / 40)))
            print('goal: {},{}'.format(goal_x, goal_y))
            path = AStar(math.floor(x / 40), math.floor(y / 40), goal_x, goal_y, costs).process()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if moves < len(path) and path:
        x = path[moves][0] * 40
        y = path[moves][1] * 40
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
                cost = success.render(str(costs[int(row_i/40)][int(col_i/40)]), False, (255, 255, 255))
                screen.blit(cost, (col_i, row_i))
            col_i += step
            if col_i == width:
                col_i = 0
        row_i += step
        if row_i == height:
            row_i = 0
    screen.blit(car, (x, y))

    pygame.display.flip()
    screen.fill((169, 169, 169))
    clock.tick(15)

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
    # if y >= height - car_h:
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


