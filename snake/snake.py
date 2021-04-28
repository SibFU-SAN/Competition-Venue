import copy


class Map:
    """Класс создания экземпляра примитивной карты"""

    def __init__(self, height, weight, apple_array):
        self.height = height
        self.weight = weight
        self.apple_array = apple_array

    def map(self):
        game_map_array = []
        for i in range(self.height):
            game_map_array.append([])
            for _ in range(self.weight):
                game_map_array[i].append(' ')
        for i in range(self.height):
            for j in range(self.weight):
                if i == 0 or i == self.height - 1:
                    game_map_array[i][j] = '▖'
                elif j == 0 or j == self.weight - 1:
                    game_map_array[i][j] = '▖'
        for i in range(len(self.apple_array)):
            game_map_array[int(self.apple_array[i][0])][int(
                self.apple_array[i][1])] = '◎'
        return game_map_array


class SnakePlayer:
    """Класс для создания экземпляра змейки"""
    def __init__(self, map_settings, snake_pos, apple, way):
        self.game_map_ARRAY = map_settings
        self.snake_position = snake_pos
        self.way = way
        self.around = 0
        self.apples = apple
        self.server_info = []

    def snake_move_forward(self):
        """Метод для движения змейки прямолинейно
        1 - Вверх, 2 - Вниз, 3 - Влево, 4 - Вправо"""

        warning = 0
        self.game_map_ARRAY[self.snake_position[0][0]][
            self.snake_position[0][1]] = '🐸'
        for i in range(len(self.snake_position)-1):
            if i != 0:
                self.game_map_ARRAY[self.snake_position[-1][0]][
                    self.snake_position[-1][1]] = '◻'
        "Проверка на то, ела ли змейка"
        self.eating()

        snake_head = [self.snake_position[0][0], self.snake_position[0][1]]

        "Очистка змейки"
        for i in range(len(self.snake_position)):
            self.game_map_ARRAY[self.snake_position[i][0]][
                self.snake_position[i][1]] = ' '

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
                self.game_map_ARRAY[self.snake_position[i][0]][
                    self.snake_position[i][1]] = '🐸'
            else:
                self.game_map_ARRAY[self.snake_position[i][0]][
                    self.snake_position[i][1]] = '◻'
        "Проверка на столкновение со стенами и с собой"
        for i in range(len(self.game_map_ARRAY)):
            if self.game_map_ARRAY[self.snake_position[0][0]][
             self.snake_position[0][1]] == self.game_map_ARRAY[i][0]:
                warning += 1
            elif self.game_map_ARRAY[self.snake_position[0][0]][
             self.snake_position[0][1]] == self.game_map_ARRAY[i][9]:
                warning += 1
            elif self.game_map_ARRAY[self.snake_position[0][0]][
             self.snake_position[0][1]] == self.game_map_ARRAY[0][i]:
                warning += 1
            elif self.game_map_ARRAY[self.snake_position[0][0]][
             self.snake_position[0][1]] == self.game_map_ARRAY[9][i]:
                warning += 1

        "Проверка на столкновение с собой"
        for i in range(len(self.snake_position)):
            if i != 0:
                if self.snake_position[0] == self.snake_position[i]:
                    warning += 1

        "Выход из игры при гибели и печать массива"
        if warning != 0:
            self.snake_position = ['stop']

        return self.snake_position, self.way

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

        return self.snake_position, self.way

    def plus_size(self, snake_pos):
        """Метод для увеличения длины змейки"""
        old_snake_position = copy.deepcopy(snake_pos)
        new_snake_position = []
        for i in range(len(self.snake_position)+1):
            if i == 0:
                if self.way == 1:
                    snake_pos[0][0] -= 1
                elif self.way == 2:
                    snake_pos[0][0] += 1
                elif self.way == 3:
                    snake_pos[0][1] -= 1
                elif self.way == 4:
                    snake_pos[0][1] += 1
                new_snake_position.append(snake_pos[i])
            elif i != len(snake_pos):
                new_snake_position.append(old_snake_position[i-1])
            elif i == len(snake_pos):
                new_snake_position.append(snake_pos[i-1])

        return new_snake_position

    def eating(self):
        """Метод для изменения данных при увеличении змейки"""
        for i in range(len(self.apples)):
            if self.game_map_ARRAY[self.snake_position[0][0]][
             self.snake_position[0][1]] == self.game_map_ARRAY[
             self.apples[i][0]][self.apples[i][1]]:
                self.snake_position = self.plus_size(self.snake_position)
                for j in range(len(self.snake_position)):
                    if j == 0:
                        self.game_map_ARRAY[self.snake_position[j][0]][
                            self.snake_position[j][1]] = '🐸'
                    else:
                        self.game_map_ARRAY[self.snake_position[j][0]][
                            self.snake_position[j][1]] = '◻'
