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
    """
    Обработка коллизий
    :returns True or False
    """
    global snake_position, map_1
    if [snake_position[0][0], snake_position[0][1]] in wall:
        return True
    return False


def snake_vision():
    """Создание поля зрения змейки"""
    global snake_position, map_1
    if ['stop'] != snake_position:
        rad = 2
        snake_vis = []
        left_angle = [snake_position[0][0] - rad, snake_position[0][1] - rad]
        for rows in range(rad + rad + 1):
            snake_vis.append([])
            for col in range(rad + rad + 1):
                if left_angle[0] + rows >= 0 and left_angle[1] + col >= 0 and left_angle[0] <= 9 and left_angle[1] <= 9:
                    snake_vis[rows].append(map_1[left_angle[0] + rows][left_angle[1] + col])
            print('  '.join(snake_vis[rows]))
        print()


def move_left():
    """Движение влево"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_around(3)
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def move_up():
    """Движение вверх"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_around(1)
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def move_down():
    """Движение влево"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_around(2)
        server_info.append(copy.deepcopy(snake_position))

    if not collision():
        snake_vision()


def move_right():
    """Движение вправо"""
    global snake_position, direction, apples_arr, map_1, server_info
    if ['stop'] != snake_position:
        snake_position, direction = snake_position, direction \
            = SnakePlayer(map_1, snake_position, apples_arr, direction). \
            snake_move_around(4)
        server_info.append(copy.deepcopy(snake_position))

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


def wall_is_left(rad=1):
    """Обнаружение стены слева
    :returns True or False"""
    global snake_position, wall
    for step in range(len(wall)):
        if [snake_position[0][0], snake_position[0][1] - rad] == wall[step]:
            return True

    return False


def wall_is_right(rad=1):
    """Обнаружение стены справа"""
    global snake_position, wall
    for step in range(len(wall)):
        if [snake_position[0][0], snake_position[0][1] + rad] == wall[step]:
            return True

    return False


def wall_is_up(rad=1):
    """Обнаружение стены сверху"""
    global snake_position, wall
    for step in range(len(wall)):
        if [snake_position[0][0] - rad, snake_position[0][1]] == wall[step]:
            return True

    return False


def wall_is_down(rad=1):
    """Обнаружение стены снизу"""
    global snake_position, wall
    for step in range(len(wall)):
        if [snake_position[0][0] + rad, snake_position[0][1]] == wall[step]:
            return True

    return False


def food(rad=1):
    """Функция для нахождения еды в поле зрения змейки"""
    global snake_position, map_1
    for rows in range(-3, 4):
        for col in range(-3, 4):
            while rad >= 1:
                if map_1[snake_position[0][0] + rad][snake_position[0][1]] == '◎':
                    return True
                elif map_1[snake_position[0][0] - rad][snake_position[0][1]] == '◎':
                    return True
                elif map_1[snake_position[0][0]][snake_position[0][1] + rad] == '◎':
                    return True
                elif map_1[snake_position[0][0]][snake_position[0][1] - rad] == '◎':
                    return True
                elif map_1[snake_position[0][0] + rad][snake_position[0][1] + rad] == '◎':
                    return True
                elif map_1[snake_position[0][0] - rad][snake_position[0][1] + rad] == '◎':
                    return True
                elif map_1[snake_position[0][0] + rad][snake_position[0][1] - rad] == '◎':
                    return True
                elif map_1[snake_position[0][0] - rad][snake_position[0][1] - rad] == '◎':
                    return True
                rad -= 1

    return False


if __name__ == '__main__':
    __builtins__.__dict__['__import__'] = None
    with open("user.txt", "r", encoding="utf-8") as file:
        code = file.read()
        exec(compile(code, "", "exec"),
             {"__cached__": None, "__doc__": None, "__file__": None,
              "__name__": None, "__loader__": None, "__package__": None,
              "__spec__": None},
             {"move_left": move_left, "move_up": move_up,
              "move_down": move_down, "move_right": move_right,
              "food": food, "move": move, "wall_is_up": wall_is_up,
              "wall_is_down": wall_is_down, "wall_is_right": wall_is_right,
              "wall_is_left": wall_is_left})

    if ['stop'] not in server_info:
        server_info.append(['stop'])

    with open("single_user.txt", "+a", encoding="utf-8") as user:
        user.write(str(server_info)+',')
