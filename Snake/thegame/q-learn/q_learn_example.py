import numpy as np
import random

# R = State diagram with goal state (mat)
# Q = minimum path from any initial state to the goal state (mat)

# gammma = learning parameter


frame_size_x = 5
frame_size_y = 5

direction_ids = {'UP': 0,
                 'RIGHT': 1,
                 'DOWN': 2,
                 'LEFT': 3}


def initialize_reward_table(frame_x_size, frame_y_size, food_pos):

    R = np.zeros((frame_y_size, frame_x_size), dtype=np.uint8)
    for idx, food in enumerate(food_pos):
        # R[food[0]][food[1]] = 1*(idx + 1)
        R[food[0]][food[1]] = food[2]

    return R

def get_possible_actions(table, current_pos):

    rewards = np.asarray([])
    try:
        # 1 = up, 2 = right, 3 = down, 4 = left
        actions = [(-1, 0, 'UP'), (0, 1, 'RIGHT'), (1, 0, 'DOWN'), (0, -1, 'LEFT')]
        # actions = []

        # UP
        # if current_pos[0] != 0:
        #     actions.append((-1, 0, 'UP'))

        # RIGHT
        # if current_pos[1] != (frame_size_x - 1):
        #     actions.append((0, 1, 'RIGHT'))

        # DOWN
        # if current_pos[0] != (frame_size_y - 1):
        #     actions.append((1, 0, 'DOWN'))

        # if current_pos[1] != 0:
        #     actions.append((0, -1, 'LEFT'))

        rewards = []
        for action in actions:

            next_pos_y = current_pos[0] + action[0]
            next_pos_x = current_pos[1] + action[1]

            if next_pos_y > frame_size_y - 1:
                next_pos_y = frame_size_y - 1

            if next_pos_y < 0:
                next_pos_y = 0

            if next_pos_x > frame_size_x - 1:
                next_pos_x = frame_size_x - 1

            if next_pos_x < 0:
                next_pos_x = 0

            # reward = table[current_pos[0] + action[0]][current_pos[1] + action[1]][direction_ids[action[2]]]
            # next_pos_y = min(max(current_pos[0] + action[0], 0), frame_size_y - 1)
            # next_pos_x = min(max(current_pos[1] + action[1], 0), frame_size_x - 1)

            expected_reward = table[direction_ids[action[2]], next_pos_y, next_pos_x]
            # expected_reward = R[current_pos[0] + action[0], current_pos[1] + action[1]]
            rewards.append([action, expected_reward])

    except Exception as err:
        print()



    return np.asarray(rewards)


# def update_q_table(table, rewards, current_position, alpha, gamma):
#     """ Algorithm """
#
#     rewards = get_possible_actions(R, current_position)
#     print("asd")
#
#     # (1 - alpha) * q(s, a) + alpha*(Reward_t+1 + gamma*max(q(s',a'))
#     # new_q_value = ((1 - alpha) * table[current_position[0], current_position[1]]
#     #                + alpha * )

#
# def perform_action(table, current_point, action):
#
#     next_point = [current_point[0] + action[0][0], current_point[1] + action[0][1]]
#
#
#     return 0, 0, 0, 0
#

if __name__ == '__main__':

    foods = [[1, 1, 1], [frame_size_y - 2, frame_size_x - 2, 2], [0, frame_size_x - 1, 10]]#, [0, frame_size_x - 1, 10]]#, [0, frame_size_x - 1], [frame_size_y - 1, 0]]
    traps = []

    # Rewards
    R = initialize_reward_table(frame_size_x, frame_size_y, foods)

    # Learning rate
    alpha = 0.1

    # discount
    gamma = 0.6

    # Q-Table
    table = np.zeros((4, frame_size_y, frame_size_x), dtype=np.float32)
    print(R)

    for i in range(1, 20):

        current_point = [np.random.randint(0, 5), 0]
        epochs, penalties, reward, = 0, 0, 0
        done = False

        epsilon = 0.99

        while not done:

            try:
                # print('Get actions')
                actions = get_possible_actions(table, current_point)

                # vis_table = table.copy()
                # vis_table = np.zeros((frame_size_y, frame_size_x))
                # vis_table[current_point[0], current_point[1]] = '11'

                # print(vis_table)
                # Ranodom action
                if random.uniform(0, 1) < epsilon:
                    action = random.choice(actions)

                else:
                    if np.sum(actions[:, 1]) == 0:
                        action = random.choice(actions)
                    else:
                        action = actions[np.argmax(actions[:, 1])]

                # print(action)
                # print(current_point)
                # print('Get next point')

                next_pos_y = current_point[0] + action[0][0]
                next_pos_x = current_point[1] + action[0][1]

                if next_pos_y > frame_size_y - 1:
                    next_pos_y = frame_size_y - 1

                if next_pos_y < 0:
                    next_pos_y = 0

                if next_pos_x > frame_size_x - 1:
                    next_pos_x = frame_size_x - 1

                if next_pos_x < 0:
                    next_pos_x = 0

                # next_point = [current_point[0] + action[0][0], current_point[1] + action[0][1]]
                next_point = [next_pos_y, next_pos_x]


                # print(next_point)
                # print('Get reward')

                # current_q_value = table[current_point[0], current_point[1]][direction_ids[action[0][2]]]
                current_q_value = table[direction_ids[action[0][2]], current_point[0], current_point[1]]
                next_reward = R[next_point[0], next_point[1]]
                # next_q_value = table[direction_ids[action[0][2]], next_point[0], next_point[1]]
                next_q_value = np.max(table[:, next_point[0], next_point[1]])
                new_value = current_q_value + alpha * (next_reward + gamma * next_q_value - current_q_value)

                current_reward = R[current_point[0], current_point[1]]

                table[direction_ids[action[0][2]], current_point[0], current_point[1]] = new_value

                current_point = next_point

                epochs += 1

                if epochs == 1000:
                    done = True

                epsilon *= 0.9999
                # print(epsilon)
                # if current_reward == 100:
                #     done = True

            except Exception as err:
                print(err)

        # print(table)
        # print('Epochs to finish: ', epochs)
    print(table)
    print('START TEST')

    for i in range(0, 10):
        current_point = [np.random.randint(1,5), np.random.randint(1,5)]
        test = False
        epochs = 0

        while test != True:

            vis_table = np.zeros((frame_size_y, frame_size_x))
            vis_table[current_point[0], current_point[1]] = '11'
            # print('-----------------')
            # print(vis_table)

            actions = get_possible_actions(table, current_point)

            # if random.uniform(0, 1) < epsilon:
            #     action = random.choice(actions)
            #
            # else:
            #     if np.sum(actions[:, 1]) == 0:
            #         action = random.choice(actions)
            #     else:
            #
            action = actions[np.argmax(actions[:, 1])]

            # print(actions)

            next_point = [current_point[0] + action[0][0], current_point[1] + action[0][1]]

            current_reward = R[current_point[0], current_point[1]]

            current_point = next_point

            epochs += 1

            # if epochs == 10:
            #     print()

            # print(current_reward)
            if current_reward == 10:
                print('EPOCHS: ', epochs)
                test = True
                print('GOAL')
