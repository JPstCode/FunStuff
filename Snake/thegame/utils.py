import numpy as np
import random
from collections import defaultdict

def get_food_position(frame_size_x, frame_size_y):
    """ """
    return [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]


def check_if_lost(snake, frame_size_x, frame_size_y):
    """ """
    if snake.head_position[0] < 0 or snake.head_position[0] > frame_size_x - 10:
        return True

    if snake.head_position[1] < 0 or snake.head_position[1] > frame_size_y - 10:
        return True

    for block in snake.body[1:]:
        if snake.head_position[1] == block[1] and snake.head_position[0] == block[0]:
            return True

    return False


def get_best_direction(start, end):
    """
    example, up direction = [1, 0], down direction = [-1, 0]
    """
    # x, y
    direction = [0, 0]
    diffs = [0, 0]

    # x
    if start[0] < end[0]:
        direction[0] = 1
    elif start[0] > end[0]:
        direction[0] = -1

    diffs[0] = abs(start[0] - end[0])

    # y
    if start[1] < end[1]:
        direction[1] = 1
    elif start[1] > end[1]:
        direction[1] = -1

    # diffs[1] = abs(start[1] - end[1])
    #
    # if diffs[0] > diffs[1]:
    #     direction[1] = 0
    # else:
    #     direction[0] = 0

    return direction

def distance_to_point(start, end):

    steps_x = abs(start[0] - end[0]) / 10
    steps_y = abs(start[1] - end[1]) / 10

    dst = steps_x + steps_y

    return dst

def route_to_commands(start, route):

    current_pos = start
    commands = []
    for i in range(0, len(route)):
        direction = get_best_direction(current_pos, route[i])
        if direction[0] != 0:
            if direction[0] == 1:
                commands.append('RIGHT')
            else:
                commands.append('LEFT')
        else:
            if direction[1] == 1:
                commands.append('DOWN')
            else:
                commands.append('UP')
        current_pos = route[i]

    return commands







### Route Algorithms

def find_path(goal, current_pos, obstacles, frame_x, frame_y):


    steps_list = []
    connections = []
    connection_id = 1
    connection_map = []
    finished = False
    iter = 0

    directions = [(10, 0), (0, 10), (-10, 0), (0, -10)]

    latest_pos = current_pos
    visited_positions = [current_pos]
    goal_reached = False
    goal_id = 0
    while True:

        if not steps_list:
            steps_list.append([])
            connections.append([])
            connection_map.append([])
            for dir_id, direction in enumerate(directions):
                pos = [current_pos[0] + direction[0], current_pos[1] + direction[1]]
                if pos not in obstacles:
                    if pos[0] > 0 and pos[0] < frame_x and pos[1] > 0 and pos[1] < frame_y:
                        steps_list[-1].append(pos)
                        visited_positions.append(pos)
                        connections[-1].append(connection_id)
                        connection_map[-1].append(str(dir_id + 1))
                        connection_id += 1
                        if pos == goal:
                            goal_reached = True
                            goal_id = connection_id
                            break
            if goal_reached:
                break

        else:
            steps_list.append([])
            connections.append([])
            connection_map.append([])
            for idx, pos in enumerate(steps_list[-2]):
                for dir_id, direction in enumerate(directions):
                    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
                    if new_pos not in obstacles:
                        if new_pos not in visited_positions:
                            if new_pos[0] > 0 and new_pos[0] < frame_x and new_pos[1] > 0 and new_pos[1] < frame_y:
                                steps_list[-1].append(new_pos)
                                visited_positions.append(new_pos)
                                # dst = distance_to_point(new_pos, current_pos)
                                connections[-1].append(connections[-2][idx])
                                connection_map[-1].append(connection_map[-2][idx] + str(dir_id + 1))
                                if new_pos == goal:
                                    goal_reached = True
                                    goal_id = connections[-2][idx]
                                    break
                if goal_reached:
                    break

            if goal_reached:
                break

    route_map = {'1': 'RIGHT',
                 '2': 'DOWN',
                 '3': 'LEFT',
                 '4': 'UP'}
    commands = []
    goal_map = connection_map[-1][-1]
    # print(goal_map)
    for step in connection_map[-1][-1]:
        # print(route_map[step])
        commands.append(route_map[step])

    return commands

    # print

    #
    # # Add goal
    # route.append(steps_list[-1][-1])
    #
    #
    #
    #
    #
    # for step_id, connection_list in enumerate(connections):
    #     for position_id, connection in enumerate(connection_list):
    #         if connection != goal_id:
    #             continue
    #         else:
    #             if step_id + 1 == len(steps_list):
    #                 route.append(steps_list[step_id][-1])
    #                 break
    #             else:
    #                 route.append(steps_list[step_id][position_id])
    #                 break
    #
    # #
    # print current_pos
    # print route
    #
    # commands = route_to_commands(current_pos, route)
    # print commands
    # print goal
    # return commands