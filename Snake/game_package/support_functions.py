import numpy as np


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


def pathfinder(snake, pathtype, food_pos, points, adjacent_points, coords, adjacent_coords):

    if pathtype == 'brute':
        route = find_bf_route(snake, food_pos, points, adjacent_points, adjacent_coords)
    else:
        route = []

    return route


# Brute Focre
def find_bf_route(snake, end_coord, points, adjacent_points, adjacent_coords):

    route = []
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

