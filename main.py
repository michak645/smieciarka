import math
import numpy
import pygame
import sys

pygame.init()

pygame.font.init()
success = pygame.font.SysFont('Comic Sans MS', 30)
text_success = success.render('Success', False, (255, 255, 255))

width, height = 400, 400
screen = pygame.display.set_mode((width, height))
x = 0
y = 0
step = 40

car_w = 40
car_h = 40

car = pygame.image.load('resources/car.png')
car = pygame.transform.scale(car, (car_w, car_h))
can = pygame.image.load('resources/can.png')
can = pygame.transform.scale(can, (car_w, car_h))
garbage = pygame.image.load('resources/garbage.jpg')
garbage = pygame.transform.scale(garbage, (car_w, car_h))

clock = pygame.time.Clock()

board = numpy.arange(100).reshape(10, 10)

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


def can_move_up(x, y):
    if obstacles[int(y / step) - 1][int(x / step)] == 0:
        return True
    else:
        return False


def can_move_down(x, y):
    y = int(y / step)
    x = int(x / step)
    if y + 1 >= 10:
        return False
    if obstacles[y + 1][x] == 0:
        return True
    else:
        return False


def can_move_left(x, y):
    if obstacles[int(y / step)][int(x / step) - 1] == 0:
        return True
    else:
        return False


def can_move_right(x, y):
    x = int(x / step)
    y = int(y / step)
    if x + 1 >= 10:
        return False
    if obstacles[y][x + 1] == 0:
        return True
    else:
        return False


garbageA_x = 2 * step
garbageA_y = 7 * step

garbageB_x = 5 * step
garbageB_y = 5 * step

garbageC_x = 6 * step
garbageC_y = 9 * step

clear = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w:
        #         if can_move_up(x, y):
        #             y -= step
        #     if event.key == pygame.K_s:
        #         if can_move_down(x, y):
        #             y += step
        #     if event.key == pygame.K_a:
        #         if can_move_left(x, y):
        #             x -= step
        #     if event.key == pygame.K_d:
        #         if can_move_right(x, y):
        #             x += step

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        if can_move_up(x, y):
            y -= step
    if pressed[pygame.K_s]:
        if can_move_down(x, y):
            y += step
    if pressed[pygame.K_a]:
        if can_move_left(x, y):
            x -= step
    if pressed[pygame.K_d]:
        if can_move_right(x, y):
            x += step

    if y >= height - car_h:
        y = height - step
    elif y < 0:
        y = 0
    if x > width - car_w:
        x = width - car_w
    elif x < 0:
        x = 0

    position = board[math.ceil(x / step), math.ceil(y / step)]

    row_i = 0
    col_i = 0
    for row in obstacles:
        for cell in row:
            if cell == 1:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (col_i, row_i, step, step)
                )
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
        screen.blit(
            text_success,
            ((width / 2) - 50, (height / 2) - 50)
        )

    pygame.display.flip()
    screen.fill((0, 0, 0))
    clock.tick(20)
