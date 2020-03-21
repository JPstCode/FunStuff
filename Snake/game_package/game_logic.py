import pygame
import sys
import random

import support_funcitons

def game(snake):

    # Difficulty settings
    # Easy      ->  10
    # Medium    ->  25
    # Hard      ->  40
    # Harder    ->  60
    # Impossible->  120
    difficulty = 25

    # Window size
    frame_size_x = 300
    frame_size_y = 300

    points, adjacent_points, coords, adjacent_coords = support_funcitons.get_adjacent_list(frame_size_x, frame_size_x)
    # route = hamiltonian_route(points,adjacent_list)

    # Checks for errors encountered
    check_errors = pygame.init()
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print('[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')

    # Initialise game window
    pygame.display.set_caption('Snake Eater')
    game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

    # Colors (R, G, B)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    # Game variables

    # head_pos = [100, 50]
    # snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    #    snake = Snake_Class.Snake([100, 50], [[100, 50], [100-10, 50], [100-(2*10), 50]])

    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    snake.eaten = False

    direction = 'RIGHT'
    change_to = direction

    score = 0
    iterator = 0
    route = []
    # Main logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game

                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # # Making sure the snake cannot move in the opposite direction instantaneously
        # if change_to == 'UP' and direction != 'DOWN':
        #     direction = 'UP'
        # if change_to == 'DOWN' and direction != 'UP':
        #     direction = 'DOWN'
        # if change_to == 'LEFT' and direction != 'RIGHT':
        #     direction = 'LEFT'
        # if change_to == 'RIGHT' and direction != 'LEFT':
        #     direction = 'RIGHT'

        # if len(route) == 0:
        #     print "moving to", change_to
        #     snake.move_snake(change_to)
        #     route = pathfinder(food_pos, points, adjacent_points, coords ,adjacent_coords)
        # else:
        #     print 'moving to,', route[iterator]
        #     snake.move_snake(route[iterator])
        #     iterator += 1

        #
        # # Move snake
        #
        # iterator += 1

        snake.move_snake(change_to)

        # Snake body growing mechanism
        snake.check_grow(food_pos)

        # Spawning food on the screen
        if snake.eaten:
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
            score += 1
            iterator = 0
            route = []
        snake.eaten = False

        # GFX
        game_window.fill(black)
        for iter, pos in enumerate(snake.body):
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            if iter == 0:
                pygame.draw.rect(game_window, white, pygame.Rect(pos[0], pos[1], 10, 10))
            else:
                pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # if len(route) == 0:
        #     route = pathfinder(food_pos, points, adjacent_points, coords ,adjacent_coords)
        #
        # # Move snake
        # snake.move_snake(route[iterator])
        #
        # iterator += 1
        if not route:
            route = support_funcitons.pathfinder(snake,'brute',food_pos, points,
                                                 adjacent_points, coords,
                                                 adjacent_coords)
            iterator = 0

        if route:
            change_to = route[iterator]
            iterator += 1

        # Game Over conditions
        # Getting out of bounds
        if snake.head_pos[0] < 0 or snake.head_pos[0] > frame_size_x - 10:
            # game_over()
            print('rippista')
            print(score)
            break
        if snake.head_pos[1] < 0 or snake.head_pos[1] > frame_size_y - 10:
            print('rippista')
            print(score)
            break

        # Touching the snake body

        dead = 0
        for block in snake.body[1:]:
            if snake.head_pos[1] == block[1] and snake.head_pos[0] == block[0]:
                # game_over()
                print('rippista')
                print(score)
                dead = 1
                break

        if dead == 1:
            break

        # show_score(1, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)

