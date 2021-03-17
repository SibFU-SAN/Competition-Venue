from snake_game import SnakePlayer, Map
import copy


server_info = []
snake_position = [[4, 3], [5, 3]]
apples = [[7, 2], [2, 2], [2, 7], [7, 7]]
map_1 = Map(10, 10, apples).map()
direction = 1


def move_left():
    global snake_position, direction, apples, map_1, server_info
    if ['stop'] not in snake_position:
        snake_position, direction = snake_position, direction\
            = SnakePlayer(map_1, snake_position, apples, direction).\
            snake_move_around(3)
        server_info.append(copy.deepcopy(snake_position))


def move_up():
    global snake_position, direction, apples, map_1, server_info
    if ['stop'] not in snake_position:
        snake_position, direction = snake_position, direction\
            = SnakePlayer(map_1, snake_position, apples, direction).\
            snake_move_around(1)
        server_info.append(copy.deepcopy(snake_position))


def move_down():
    global snake_position, direction, apples, map_1, server_info
    if ['stop'] not in snake_position:
        snake_position, direction = snake_position, direction\
            = SnakePlayer(map_1, snake_position, apples, direction).\
            snake_move_around(2)
        server_info.append(copy.deepcopy(snake_position))


def move_right():
    global snake_position, direction, apples, map_1, server_info
    if ['stop'] not in snake_position:
        snake_position, direction = snake_position, direction\
            = SnakePlayer(map_1, snake_position, apples, direction).\
            snake_move_around(4)
        server_info.append(copy.deepcopy(snake_position))


def move():
    global snake_position, direction, apples, map_1, server_info
    if ['stop'] not in snake_position:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples, direction). \
            snake_move_forward()
        server_info.append(copy.deepcopy(snake_position))


for i in range(2):
    move_left()
move_up()
move_up()
move_right()
move()
move_up()
move_up()
"Попытка ходить после смерти"
move_up()
