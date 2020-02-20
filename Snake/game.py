"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random, Snake_Class, \
    numpy as np

snake = Snake_Class.Snake([100, 50], [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]])


def get_adjacent_list(frame_size_x, frame_size_y):

    x_coords = np.arange(0, frame_size_x, 10)
    y_coords = np.arange(0, frame_size_y, 10)

    points = []
    coords = []
    iter = 0
    for i in range(0,len(x_coords)):
        points.append([])
        coords.append([])
        for j in range(0, len(y_coords)):
            points[i].append(iter)
            coords[i].append((j*10,i*10))
            iter += 1

    adjacent_points = []
    adjacent_coords = []
    for i in range(0,len(x_coords)):
        for j in range(0,len(y_coords)):
            adj_points = []
            adj_coords = []
            # Left side
            if j == 0:
                adj_points.append(points[i][j+1])
                adj_coords.append(coords[i][j+1])
            #Right side
            elif j == (len(x_coords)-1):
                adj_points.append(points[i][j-1])
                adj_coords.append(coords[i][j-1])
            else:
                adj_points.append(points[i][j-1])
                adj_points.append(points[i][j+1])

                adj_coords.append(coords[i][j-1])
                adj_coords.append(coords[i][j+1])

            # Top side
            if i == 0:
                adj_points.append(points[i+1][j])
                adj_coords.append(coords[i+1][j])
            # Bottom side
            elif i == (len(y_coords)-1):
                adj_points.append(points[i-1][j])
                adj_coords.append(coords[i - 1][j])
            else:
                adj_points.append(points[i-1][j])
                adj_points.append(points[i+1][j])

                adj_coords.append(coords[i - 1][j])
                adj_coords.append(coords[i + 1][j])

            adjacent_points.append(np.asanyarray(adj_points))
            adjacent_coords.append(np.asanyarray(adj_coords))

    return np.asanyarray(points), np.asanyarray(adjacent_points),\
           np.asanyarray(coords), np.asanyarray(adjacent_coords)


def hamiltonian_route(points, adjacents):

    start_point = points[snake.head_pos[1]/10][snake.head_pos[0]/10]
    options = adjacents[start_point]



    print "asd"


# Brute Focre
def find_bf_route(points, end_coord, adjacents, coords, adjacent_coords):


    route = []
    end_point = points[food_pos[1]/10][food_pos[0]/10]
    current_point = points[snake.head_pos[1]/10][snake.head_pos[0]/10]
    snake_direction = snake.direction

    while True:
        possible_coords = adjacent_coords[current_point]
        possible_points = adjacent_points[current_point]
        if len(possible_coords) == 4:
            direction_map = ['LEFT','RIGHT', 'UP', 'DOWN']
        else:
            top_row = points[0,:]
            left_col = points[:,0]
            bot_row = points[-1,:]
            right_col = points[:,-1]

            if current_point in top_row and current_point not in left_col and current_point not in right_col:
                direction_map = ['LEFT', 'RIGHT', 'DOWN']
            elif current_point in top_row and current_point in left_col:
                direction_map = ['RIGHT', 'DOWN']
            elif current_point in top_row and current_point in right_col:
                direction_map = ['LEFT', 'DOWN']

            elif current_point in left_col and current_point not in top_row and current_point not in bot_row:
                direction_map = ['RIGHT', 'DOWN', 'UP']
            elif current_point in left_col and current_point in bot_row:
                direction_map = ['RIGHT', 'UP']

            elif current_point in bot_row and current_point not in left_col and current_point not in right_col:
                direction_map = ['LEFT', 'RIGHT', 'UP']
            elif current_point in bot_row and current_point in right_col:
                direction_map = ['LEFT', 'UP']

            elif current_point in right_col and current_point not in top_row and current_point not in bot_row:
                direction_map = ['LEFT', 'UP', 'DOWN']


        distances = []
        for possible in possible_coords:
#            distance = np.linalg.norm(possible - end_coord)
            dx = abs(end_coord[1] - possible[1])
            dy = abs(end_coord[0] - possible[0])
            #distance = np.sqrt(dx**2 + dy**2)
            distance = dx + dy
            distances.append(distance)

        choices = np.argsort(distances)
        best_choice = choices[0]
        best_direction = direction_map[best_choice]

        if (snake_direction == 'RIGHT' and best_direction == 'LEFT') or \
                (snake_direction == 'LEFT' and best_direction == 'RIGHT') or \
                (snake_direction == 'DOWN' and best_direction == 'UP') or \
                (snake_direction == 'UP' and best_direction == 'DOWN'):
            best_choice = choices[1]
            best_direction = direction_map[best_choice]


        route.append(best_direction)
        snake_direction = best_direction
        current_point = possible_points[best_choice]

        if distances[best_choice] == 0.0:
            print "yaass"
            break

    return route
    #
    #
    # print "Finding Route"
    # while True:
    #
    #     # Left, Right, Up, Down
    #     possibilities = adjacent_coords[location]
    #     possibility_points = adjacents[location]
    #
    #     if len(possibilities) == 4:
    #         direction_map = ['LEFT', 'RIGHT', 'UP', 'DOWN']
    #
    #     elif len(possibilities) == 3:
    #         print "asd"
    #
    #     else:
    #         print "asdas"
    #
    #
    #     distances = []
    #     for possibility in possibilities:
    #         distance = np.linalg.norm(possibility-end)
    #         distances.append(distance)
    #
    #     choices = np.argsort(distances)
    #     best_direction = choices[0]
    #
    #     route.append(direction_map[best_direction])
    #     location = possibility_points[best_direction]
    #     location_coords = possibilities[best_direction]
    #     snake_direction = direction_map[best_direction]
    #
    #     if np.linalg.norm(location_coords-end) == 0:
    #         break
    #
    # print "Found"
    # return route




def pathfinder(food_pos, points, adjacent_points, coords, adjacent_coords):

    # https://www.pantechsolutions.net/ai-snake-game-design-using-machine-learning
    start_point = points[snake.head_pos[1]/10][snake.head_pos[0]/10]
    food_loc = points[food_pos[1]/10][food_pos[0]/10]

    #food_pos[0] = food_pos[0]/10
    #food_pos[1] = food_pos[1]/10



    route = find_bf_route(points, food_pos, adjacent_points, coords, adjacent_coords)

    if route:
        return route











if __name__ == '__main__':

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

    points, adjacent_points, coords, adjacent_coords = get_adjacent_list(frame_size_x, frame_size_x)
    #route = hamiltonian_route(points,adjacent_list)

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

    #head_pos = [100, 50]
    #snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
#    snake = Snake_Class.Snake([100, 50], [[100, 50], [100-10, 50], [100-(2*10), 50]])


    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
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
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
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
            route = pathfinder(food_pos, points, adjacent_points, coords, adjacent_coords)
            iterator = 0

        if route:
            change_to = route[iterator]
            iterator += 1

        # Game Over conditions
        # Getting out of bounds
        if snake.head_pos[0] < 0 or snake.head_pos[0] > frame_size_x-10:
            #game_over()
            print('rippista')
            print(score)
            break
        if snake.head_pos[1] < 0 or snake.head_pos[1] > frame_size_y-10:
            print('rippista')
            print(score)
            break

        # Touching the snake body

        dead = 0
        for block in snake.body[1:]:
            if snake.head_pos[1] == block[1] and snake.head_pos[0] == block[0]:
                #game_over()
                print('rippista')
                print(score)
                dead = 1
                break

        if dead == 1:
            break

        #show_score(1, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)