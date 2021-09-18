import os
import random
import sys

import pygame

from thegame.snake import Snake
from thegame.utils import get_food_position, check_if_lost, a_star_path

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)


class Game:
    def __init__(self, frame_x_size, frame_y_size, difficulty, snake, food_pos):

        self.frame_x_size = frame_x_size
        self.frame_y_size = frame_y_size
        self.snake = snake
        self.food_position = food_pos
        self.difficulty = difficulty
        self.game_lost = False

        pygame.display.set_caption('Snake game')
        self.game_window = pygame.display.set_mode((self.frame_x_size,
                                                    self.frame_y_size))

        # self.game_window = pygame.display
        # self.game_window.set_mode((self.frame_x_size, self.frame_y_size))

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        self.check_errors()
        self.draw_elements()
        self.update_game()

    def draw_elements(self):

        # Draw snake body
        self.game_window.fill(black)
        for iter, pos in enumerate(self.snake.body):
            if iter == 0:
                pygame.draw.rect(self.game_window, white, pygame.Rect(pos[0], pos[1], 10, 10))
            else:
                pygame.draw.rect(self.game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw food
        pygame.draw.rect(self.game_window, red, pygame.Rect(self.food_position[0],
                                                            self.food_position[1], 10, 10))

    # @staticmethod
    def update_game(self):

        self.snake.move(self.snake.direction)
        self.snake.grow(self.food_position)
        self.draw_elements()
        self.game_lost = check_if_lost(self.snake, self.frame_y_size, self.frame_x_size)
        print(self.game_lost)
        if self.game_lost:
            print()
            check_if_lost(self.snake, self.frame_y_size, self.frame_x_size)
            print()
        pygame.display.update()
        self.fps_controller.tick(self.difficulty)

        # print()

    def grow_snake(self):
        # self.snake.grow(self.food_position)
        food_in_snake = True
        while food_in_snake:
            self.food_position = [random.randrange(1, (self.frame_x_size // 10)) * 10,
                                  random.randrange(1, (self.frame_y_size // 10)) * 10]

            if self.food_position not in self.snake.body:
                food_in_snake = False
                self.snake.eaten = False
                self.draw_elements()
                # print()
                # self.draw_elements()
                # break

    @staticmethod
    def check_errors():

        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors
        if check_errors[1] > 0:
            print('[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')

    @staticmethod
    def get_event():
        return pygame.event.get()

    # @staticmethod
    # def update():
    #     pygame.display.update()

if __name__ == '__main__':

    frame_x = 300
    frame_y = 300
    diff = 20

    direction = 'RIGHT'
    new_direction = direction
    snake = Snake([100, 50], direction, [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]])
    food_pos = get_food_position(frame_x, frame_y)
    game = Game(frame_x, frame_y, diff, snake, food_pos)
    # game.update_game()
    route = []

    while not game.game_lost:
        # game.snake.direction = direction
        # game.update_game()
        if not route:
            route = a_star_path(game.food_position, game.snake.head_position,
                                game.snake.body[1:], frame_x, frame_y)
        else:
            print(route)
            for direction in route:
                game.snake.direction = direction
                game.update_game()

                if game.snake.eaten:
                    game.grow_snake()
                    # game.update_game()
                    print(game.food_position)
                    route = []
        #             break


