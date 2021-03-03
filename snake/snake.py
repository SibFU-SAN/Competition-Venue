import time
import copy
from guppy import hpy


class Map:
    """Класс создания экземпляра примитивной карты"""

    def __init__(self, height, weight, apple_ARRAY):
        self.height = height
        self.weight = weight
        self.apple_ARRAY = apple_ARRAY

    def map(self):
        game_map_ARRAY = []
        for i in range(self.height):
            game_map_ARRAY.append([])
            for j in range(self.weight):
                game_map_ARRAY[i].append(0)
        for i in range(self.height):
            for j in range(self.weight):
                if i == 0 or i == self.height - 1:
                    game_map_ARRAY[i][j] = 1
                elif j == 0 or j == self.weight - 1:
                    game_map_ARRAY[i][j] = 1
        for i in range(len(self.apple_ARRAY)):
            game_map_ARRAY[self.apple_ARRAY[i][0]][self.apple_ARRAY[i][1]] = 5
        return game_map_ARRAY


class SnakePlayer:
    """Класс для создания экземпляра змейки"""
    def __init__(self, map_settings, snake_position, apples, way):
        self.game_map_ARRAY = map_settings
        self.snake_position = snake_position
        self.way = way
        self.around = 0
        self.apples = apples

    def snake_move_forward(self):
        """Метод для движения змейки прямолинейно
        1 - Вверх, 2 - Вниз, 3 - Влево, 4 - Вправо"""
        warning = 0
        self.game_map_ARRAY[self.snake_position[0][0]][self.snake_position[0][1]] = 3
        for i in range(len(snake_position)-1):
            if i != 0:
                self.game_map_ARRAY[self.snake_position[-1][0]][self.snake_position[-1][1]] = 2

        snake_head = []
        snake_head.append(snake_position[0][0])
        snake_head.append(snake_position[0][1])

        "Очистка змейки"
        for i in range(len(self.snake_position)):
            self.game_map_ARRAY[self.snake_position[i][0]][self.snake_position[i][1]] = 0

        "Изменение координат змейки"
        for j in range(len(self.snake_position)-1):
            self.snake_position[-j-1] = self.snake_position[-j-2]
        if self.around == 0:
            if self.way == 1:
                snake_head[0] -= 1
            elif self.way == 2:
                snake_head[0] += 1
            elif self.way == 3:
                snake_head[1] -= 1
            elif self.way == 4:
                snake_head[1] += 1

        self.snake_position[0] = snake_head

        "Рисование змейки с новыми координатами"
        for i in range(len(self.snake_position)):
            if i == 0:
                self.game_map_ARRAY[self.snake_position[i][0]][self.snake_position[i][1]] = 3
            else:
                self.game_map_ARRAY[self.snake_position[i][0]][self.snake_position[i][1]] = 2
        "Проверка на то, ела ли змейка"
        self.eating()
        "Проверка на столкновение со стенами"
        for i in range(len(self.game_map_ARRAY)):
            if self.game_map_ARRAY[self.snake_position[0][0]][self.snake_position[0][1]] == self.game_map_ARRAY[i][0]:
                warning += 1
            elif self.game_map_ARRAY[self.snake_position[0][0]][self.snake_position[0][1]] == self.game_map_ARRAY[i][9]:
                warning += 1
            elif self.game_map_ARRAY[self.snake_position[0][0]][self.snake_position[0][1]] == self.game_map_ARRAY[0][i]:
                warning += 1
            elif self.game_map_ARRAY[self.snake_position[0][0]][self.snake_position[0][1]] == self.game_map_ARRAY[9][i]:
                warning += 1

        "Выход из игры при гибели"
        if warning == 0:
            for i in range(len(self.game_map_ARRAY)):
                print(self.game_map_ARRAY[i])
            print()
        else:
            print("Game Over")
            quit()

        return self.snake_position

    def snake_move_around(self, new_way):
        """Метод для поворотов змейки
        1 - Вверх, 2 - Вниз, 3 - Влево, 4 - Вправо"""
        if new_way == 1:
            self.way = 1
        elif new_way == 2:
            self.way = 2
        elif new_way == 3:
            self.way = 3
        elif new_way == 4:
            self.way = 4

        self.snake_move_forward()

        return self.snake_position

    def plus_size(self, snake_position):
        """Метод для увеличения длины змейки"""
        old_snake_position = copy.deepcopy(snake_position)
        new_snake_position = []
        for i in range(len(snake_position)+1):
            if i == 0:
                if self.way == 1:
                    snake_position[0][0] -= 1
                elif self.way == 2:
                    snake_position[0][0] += 1
                elif self.way == 3:
                    snake_position[0][1] -= 1
                elif self.way == 4:
                    snake_position[0][1] += 1
                new_snake_position.append(snake_position[i])
            elif i != len(snake_position):
                new_snake_position.append(old_snake_position[i-1])
            elif i == len(snake_position):
                new_snake_position.append(snake_position[i-1])

        return new_snake_position

    def eating(self):
        """Метод для изменения глобальных данных при увеличении змейки"""
        for i in range(len(self.apples)):
            if self.game_map_ARRAY[snake_position[0][0]][snake_position[0][1]] ==\
                    self.game_map_ARRAY[apples[i][0]][apples[i][1]]:
                self.snake_position = self.plus_size(snake_position)
                for j in range(len(self.game_map_ARRAY)):
                    print(self.game_map_ARRAY[j])
                print()
                for j in range(len(self.snake_position)):
                    if j == 0:
                        self.game_map_ARRAY[self.snake_position[j][0]][self.snake_position[j][1]] = 3
                    else:
                        self.game_map_ARRAY[self.snake_position[j][0]][self.snake_position[j][1]] = 2


if __name__ == '__main__':
    t1 = time.time()
    snake_position = [[4, 3], [5, 3]]
    apples = [[7, 2], [2, 2], [2, 7], [7, 7]]
    map_1 = Map(10, 10, apples).map()
    snake_position = SnakePlayer(map_1, snake_position, apples, 1).snake_move_forward()
    snake_position = SnakePlayer(map_1, snake_position, apples, 1).snake_move_forward()
    snake_position = SnakePlayer(map_1, snake_position, apples, 1).snake_move_around(3)
    snake_position = SnakePlayer(map_1, snake_position, apples, 3).snake_move_around(2)
    snake_position = SnakePlayer(map_1, snake_position, apples, 2).snake_move_around(4)

    t2 = time.time()
    print(t2-t1)
    print(hpy().heap())
