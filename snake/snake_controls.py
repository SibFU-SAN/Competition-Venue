from snake_game import SnakePlayer, Map
import copy

"""Входные данные
Задаётся позиция змейки, позиции яблок, карта и направление"""
server_info = []
snake_position = [[4, 3], [5, 3]]
apples_arr = [[7, 2], [2, 2], [2, 7], [7, 7]]
map_1 = Map(10, 10, apples_arr).map()
direction = 1
wall = []

"Искуственная генерация карты"
for x in range(10):
    for y in range(10):
        if map_1[x][y] == '▖':
            wall.append([x, y])


def collision():
    global snake_position, map_1
    if [snake_position[0][0], snake_position[0][1]] in wall:
        return True
    return False


def snake_vision():
    global snake_position, map_1
    if ['stop'] != snake_position:
        rad = 2
        snake_vis = []
        left_angle = [snake_position[0][0]-rad, snake_position[0][1]-rad]
        for rows in range(rad+rad+1):
            snake_vis.append([])
            for col in range(rad+rad+1):
                if left_angle[0]+rows >= 0 and left_angle[1]+col >= 0 and left_angle[0] <= 9 and left_angle[1] <= 9:
                    snake_vis[rows].append(map_1[left_angle[0]+rows][left_angle[1]+col])
            print('  '.join(snake_vis[rows]))
        print()


def move_left():
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction\
            = SnakePlayer(map_1, snake_position, apples_arr, direction).\
            snake_move_around(3)
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def move_up():
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction\
            = SnakePlayer(map_1, snake_position, apples_arr, direction).\
            snake_move_around(1)
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def move_down():
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction\
            = SnakePlayer(map_1, snake_position, apples_arr, direction).\
            snake_move_around(2)
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def move_right():
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction\
            = SnakePlayer(map_1, snake_position, apples_arr, direction).\
            snake_move_around(4)
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def move():
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_forward()
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def wall_is_left(rad=1):
    global snake_position, wall
    for step in range(len(wall)):
        if [snake_position[0][0], snake_position[0][1]-rad] == wall[step]:
            return True

    return False


def wall_is_right(rad=1):
    global snake_position, wall
    for step in range(len(wall)):
        if [snake_position[0][0], snake_position[0][1]+rad] == wall[step]:
            return True

    return False


def wall_is_up(rad=1):
    global snake_position, wall
    for step in range(len(wall)):
        if [snake_position[0][0]-rad, snake_position[0][1]] == wall[step]:
            return True

    return False


def wall_is_down(rad=1):
    global snake_position, wall
    for step in range(len(wall)):
        if [snake_position[0][0]+rad, snake_position[0][1]] == wall[step]:
            return True

    return False


def food(rad=1):
    global snake_position, map_1
    for rows in range(-3, 4):
        for col in range(-3, 4):
            while rad >= 1:
                if map_1[snake_position[0][0]+rad][snake_position[0][1]] == '◎':
                    return True
                elif map_1[snake_position[0][0]-rad][snake_position[0][1]] == '◎':
                    return True
                elif map_1[snake_position[0][0]][snake_position[0][1]+rad] == '◎':
                    return True
                elif map_1[snake_position[0][0]][snake_position[0][1]-rad] == '◎':
                    return True
                elif map_1[snake_position[0][0]+rad][snake_position[0][1]+rad] == '◎':
                    return True
                elif map_1[snake_position[0][0]-rad][snake_position[0][1]+rad] == '◎':
                    return True
                elif map_1[snake_position[0][0]+rad][snake_position[0][1]-rad] == '◎':
                    return True
                elif map_1[snake_position[0][0]-rad][snake_position[0][1]-rad] == '◎':
                    return True
                rad -= 1

    return False


if __name__ == '__main__':
    move_left()
    move_left()
    move_left()
    move_left()
    move_left()
