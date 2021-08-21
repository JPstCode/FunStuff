import os
import numpy as np
import random
import sys

import pygame

from thegame.utils import get_food_position, check_if_lost, find_path
from thegame.snake import Snake

# Initialize game window

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 200
frame_size_y = 200

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print('[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

pygame.display.set_caption('Snake game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)


direction = 'RIGHT'
new_direction = direction
snake = Snake([100, 50], direction, [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]])

food_pos = get_food_position(frame_size_x, frame_size_y)

route = []
route_step = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Key pressed
        elif event.type == pygame.KEYDOWN:

            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                new_direction = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                new_direction = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                new_direction = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                new_direction = 'RIGHT'
            # Esc -> Create event to quit the game

            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if route:
        new_direction = route[route_step]
        route_step += 1

    # print new_direction

    snake.move(new_direction)
    snake.grow(food_pos)

    if snake.eaten:
        while True:
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
            if food_pos not in snake.body:
                route = []
                route_step = 0
                break

    snake.eaten = False

    # Draw snake body
    game_window.fill(black)
    for iter, pos in enumerate(snake.body):
        if iter == 0:
            pygame.draw.rect(game_window, white, pygame.Rect(pos[0], pos[1], 10, 10))
        else:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    if check_if_lost(snake, frame_size_x, frame_size_y):
        break

    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)

    if not route:
        route = find_path(food_pos, snake.head_position, snake.body[1:], frame_size_x, frame_size_y)
        # print route


