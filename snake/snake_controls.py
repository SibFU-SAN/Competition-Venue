import copy
from snake.snake import SnakePlayer, Map


def start_options(apples):
    """Входные данные
    Задаётся позиция змейки, позиции яблок, карта и направление"""
    map_ = Map(height, weight, apples).map()

    return map_


def map_gen():
    walls = []
    for x in range(height):
        for y in range(weight):
            if map_1[x][y] == '▖':
                walls.append([x, y])
    return walls


def collision():
    """Обработка коллизий"""
    global snake_position, map_1
    if [snake_position[0][0], snake_position[0][1]] in wall:
        return True
    return False


def snake_vision():
    """Создание поля зрения змейки"""
    global snake_position, map_1
    if ['stop'] != snake_position:
        snake_vis = []
        left_angle = [snake_position[0][0] - rad, snake_position[0][1] - rad]
        for rows in range(rad + rad + 1):
            snake_vis.append([])
            for col in range(rad + rad + 1):
                if 0 <= left_angle[0] + rows <= height-1 and 0 <= left_angle[1] + col <= weight-1:
                    snake_vis[rows].append(map_1[left_angle[0] + rows][left_angle[1] + col])
            print('  '.join(snake_vis[rows]))
        print()


def move_left():
    """Движение влево"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position and direction != 4:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_around(3)
        server_info.append(copy.deepcopy(snake_position))
        direction = 3

    if not collision():
        snake_vision()


def move_up():
    """Движение вверх"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position and direction != 2:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_around(1)
        server_info.append(copy.deepcopy(snake_position))
        direction = 1

    if not collision():
        snake_vision()


def move_down():
    """Движение влево"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position and direction != 1:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_around(2)
        server_info.append(copy.deepcopy(snake_position))
        direction = 2

    if not collision():
        snake_vision()


def move_right():
    """Движение вправо"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position and direction != 3:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_around(4)
        server_info.append(copy.deepcopy(snake_position))
        direction = 4

    if not collision():
        snake_vision()


def move():
    """Функция для продолжения движения в заданном направлении"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_forward()
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def wall_is_left(rads=1):
    """Обнаружение стены слева"""
    global snake_position, wall
    if 0 <= rads <= rad:
        if ['stop'] != snake_position:
            for step in range(len(wall)):
                if [snake_position[0][0], snake_position[0][1] - rads]\
                        == wall[step]:
                    return True
    else:
        return False

    return False


def wall_is_right(rads=1):
    """Обнаружение стены справа"""
    global snake_position, wall
    if 0 <= rads <= rad:
        if ['stop'] != snake_position:
            for step in range(len(wall)):
                if [snake_position[0][0], snake_position[0][1] + rads]\
                        == wall[step]:
                    return True
    else:
        return False

    return False


def wall_is_up(rads=1):
    """Обнаружение стены сверху"""
    global snake_position, wall
    if 0 <= rads <= rad:
        if ['stop'] != snake_position:
            for step in range(len(wall)):
                if [snake_position[0][0] - rads, snake_position[0][1]]\
                        == wall[step]:
                    return True
    else:
        return False

    return False


def wall_is_down(rads=1):
    """Обнаружение стены снизу"""
    global snake_position, wall
    if 0 <= rads <= rad:
        if ['stop'] != snake_position:
            for step in range(len(wall)):
                if [snake_position[0][0] + rads, snake_position[0][1]]\
                        == wall[step]:
                    return True
    else:
        return False

    return False


def food(rads=1):
    """Функция для нахождения еды в поле зрения змейки"""
    global snake_position, map_1
    if 0 <= rads <= rad:
        if ['stop'] != snake_position:
            for rows in range(-rads, rads):
                for col in range(-rads, rads):
                    if 0 <= snake_position[0][0] + rows <= height-1 \
                         and 0 <= snake_position[0][1] + col <= weight-1:
                        if map_1[snake_position[0][0] + rows][
                                 snake_position[0][1] + col] == '◎':
                            return True
    else:
        return False

    return False


def direction_right():
    if direction == 4:
        return True
    return False


def direction_left():
    if direction == 3:
        return True
    return False


def direction_up():
    if direction == 1:
        return True
    return False


def direction_down():
    if direction == 2:
        return True
    return False


def final():
    exec(compile(code, "", "exec"),
         {"__cached__": None, "__doc__": None, "__file__": None,
          "__name__": None, "__loader__": None, "__package__": None,
          "__spec__": None, "print": None, "exec": None,
          "eval": None},
         {"move_left": move_left, "move_up": move_up,
          "move_down": move_down, "move_right": move_right,
          "food": food, "move": move, "wall_is_up": wall_is_up,
          "wall_is_down": wall_is_down, "wall_is_right": wall_is_right,
          "wall_is_left": wall_is_left, "direction_right": direction_right,
          "direction_left": direction_left, "direction_down": direction_down,
          "direction_up": direction_up})

    if ['stop'] not in server_info:
        server_info.append(['stop'])

    with open(f"./resources/tmp/{game_hash}.txt", "+a", encoding="utf-8") as user:
        user.write(str(server_info) + ',')


if __name__ == '__main__':
    final()
    game_hash = ''
    server_info = []
    snake_position = []
    apples_arr = []
    direction = 0
    map_1 = []
    wall = []
    height = 0
    weight = 0
    code = ''
    rad = 3
