import heapq
import math
import numpy
import pygame
import sys


# define A*
class Node(object):
    def __init__(self, x, y, direction, cost):
        """
        Initialize new cell
        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.direction = direction
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = cost


class AStar(object):
    def __init__(self, startx, starty, direction, endx, endy, costs):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = 10
        self.grid_width = 10
        directions = ["N", "E", "W", "S"]
        for y in range(self.grid_height):
            self.cells.append([])
            for x in range(self.grid_width):
                self.cells[y].append([])
                for i in range(4):
                    self.cells[y][x].append(
                        Node(x, y, directions[i], costs[y][x]))
        self.start = self.get_cell(startx, starty, direction)
        self.end = self.get_cell(endx, endy, direction)

    def get_heuristic(self, cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def get_cell(self, x, y, direction):
        if direction == "N":
            return self.cells[y][x][0]
        if direction == "E":
            return self.cells[y][x][1]
        if direction == "W":
            return self.cells[y][x][2]
        if direction == "S":
            return self.cells[y][x][3]

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.direction == "N":
            if cell.y > 0:
                cells.append(self.get_cell(cell.x, cell.y - 1, cell.direction))
            cells.append(self.get_cell(cell.x, cell.y, "E"))
            cells.append(self.get_cell(cell.x, cell.y, "W"))
        elif cell.direction == "W":
            if cell.x > 0:
                cells.append(self.get_cell(cell.x - 1, cell.y, cell.direction))
            cells.append(self.get_cell(cell.x, cell.y, "N"))
            cells.append(self.get_cell(cell.x, cell.y, "S"))
        elif cell.direction == "E":
            if cell.x < 9:
                cells.append(self.get_cell(cell.x + 1, cell.y, cell.direction))
            cells.append(self.get_cell(cell.x, cell.y, "S"))
            cells.append(self.get_cell(cell.x, cell.y, "N"))
        elif cell.direction == "S":
            if cell.y < 9:
                cells.append(self.get_cell(cell.x, cell.y + 1, cell.direction))
            cells.append(self.get_cell(cell.x, cell.y, "W"))
            cells.append(self.get_cell(cell.x, cell.y, "E"))
        return cells

    def display_path(self):
        cell = self.end
        print('path:')
        path = []
        i = 0
        while cell.parent is not self.start:
            cell = cell.parent
            path.append([])
            print('cell: %d,%d,%s' % (cell.x, cell.y, cell.direction))
            x = cell.x
            y = cell.y
            d = cell.direction
            path[i].append(x)
            path[i].append(y)
            path[i].append(d)
            i = i + 1
        return path

    def update_cell(self, adj, cell):
        adj.g = cell.g + adj.cost
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                return self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g + adj_cell.cost:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


pygame.init()

pygame.font.init()
success = pygame.font.SysFont('Comic Sans MS', 30)
text_success = success.render('Success', False, (255, 255, 255))

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

# 2 dimensional array for obstacles
obstacles = numpy.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
])

# weights array
weigth = numpy.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
])


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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            goal_x = math.ceil(pos[0]/40)
            goal_y = math.ceil(pos[1]/40)
            print('{},{}'.format(goal_x, goal_y))
            path = AStar(x, y, direction, goal_x, goal_y, weigth).process()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a]:
        if direction == 'S':
            direction = 'E'
        elif direction == 'E':
            direction = 'N'
        elif direction == 'N':
            direction = 'W'
        elif direction == 'W':
            direction = 'S'
        print('direction - {}'.format(direction))

    if pressed[pygame.K_d]:
        if direction == 'S':
            direction = 'W'
        elif direction == 'E':
            direction = 'S'
        elif direction == 'N':
            direction = 'E'
        elif direction == 'W':
            direction = 'N'
        print('direction - {}'.format(direction))

    if pressed[pygame.K_w]:
        if direction == 'N' and can_move_up(x, y):
            y -= step
        elif direction == 'S' and can_move_down(x, y):
            y += step
        elif direction == 'E' and can_move_right(x, y):
            x += step
        elif direction == 'W' and can_move_left(x, y):
            x -= step

    if pressed[pygame.K_s]:
        if direction == 'N' and can_move_down(x, y):
            y += step
        elif direction == 'S' and can_move_up(x, y):
            y -= step
        elif direction == 'E' and can_move_left(x, y):
            x -= step
        elif direction == 'W' and can_move_right(x, y):
            x += step

    if y >= height - car_h:
        y = height - step
    elif y < 0:
        y = 0
    if x > width - car_w:
        x = width - car_w
    elif x < 0:
        x = 0

    position = board[math.ceil(x/step), math.ceil(y/step)]

    row_i = 0
    col_i = 0
    for row in obstacles:
        for cell in row:
            if cell == 1:
                pygame.draw.rect(screen, (255, 255, 255), (col_i, row_i, step, step))
            col_i += step
            if col_i == width:
                col_i = 0
        row_i += step
        if row_i == height:
            row_i = 0

    screen.blit(car, (x, y))
    screen.blit(can, (width - 40, height - 40))

    if x == garbageA_x and y == garbageA_y:
        garbageA_x = width - step
        garbageA_y = height - step
        clear += 1
    if x == garbageB_x and y == garbageB_y:
        garbageB_x = width - step
        garbageB_y = height - step
        clear += 1
    if x == garbageC_x and y == garbageC_y:
        garbageC_x = width - step
        garbageC_y = height - step
        clear += 1

    screen.blit(garbage, (garbageA_x, garbageA_y))
    screen.blit(garbage, (garbageB_x, garbageB_y))
    screen.blit(garbage, (garbageC_x, garbageC_y))

    if clear == 3:
        screen.fill((0, 0, 0))
        screen.blit(text_success, ((width/2)-50, (height/2)-50))

    pygame.display.flip()
    screen.fill((0, 0, 0))
    clock.tick(15)
