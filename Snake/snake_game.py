# Based on implementation: https://gist.github.com/rajatdiptabiswas/bd0aaa46e975a4da5d090b801aba0611

import pygame, sys, time, random,
from Snake_Class import SnakeClass






if __name__ == '__main__':


    frame_size_x = 800
    frame_size_y = 800

    # Checks for errors encountered
    check_errors = pygame.init()
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')

    # Init game window
    game_window = pygame.display.set_mode((frame_size_x,frame_size_y))

    # Colors

    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()



    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

    snake = SnakeClass(snake_pos, snake_body)


    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0

