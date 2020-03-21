import numpy as np

import Snake_Class
import game_logic

snake = Snake_Class.Snake([100, 50], [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]])

game_logic.game(snake)

