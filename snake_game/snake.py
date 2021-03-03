VECTOR_UP = (0, 1)
VECTOR_DOWN = (0, -1)
VECTOR_RIGHT = (1, 0)
VECTOR_LEFT = (-1, 0)


def get_vector(direction: int) -> tuple:
    """
    Возвращает вектор от номера направления
    :param direction: Номер направления
    :return: Вектор
    """
    direction = direction % 4
    if direction < 2:
        return VECTOR_UP if direction == 0 else VECTOR_RIGHT
    return VECTOR_DOWN if direction == 2 else VECTOR_LEFT


class Snake:
    def __init__(self, x: int, y: int, direction: int):
        self.head = Element(x, y, direction)

    @property
    def second_element(self):
        """
        Возвращает второй элемент змейки
        :return: Второй элемент змейки
        """
        return self.head.next_element

    @property
    def last_element(self):
        """
        Возвращает последний элемент змейки
        :return: Последний элемент змейки
        """
        temp = self.head.next_element
        while temp.next_element is not None:
            temp = temp.next_element

        return temp

    @property
    def length(self) -> int:
        """
        Возвращает длинну змейки
        :return: Длинна змейки
        """
        temp = self.head.next_element
        length = temp.distance_to_next_element
        while temp is not None:
            temp = temp.next_element
            length += temp.distance_to_next_element
        return length

    def turn_right(self) -> None:
        """
        Поворачиает голову змейки направо
        :return:
        """
        self.head.turn_right()

    def turn_left(self) -> None:
        """
        Поворачиает голову змейки налево
        :return:
        """
        self.head.turn_left()

    def move(self) -> None:
        """
        Двигает змейку на 1 элемент
        :return:
        """
        if self.head.direction != self.second_element.direction:
            new_element = Element(self.head.x, self.head.y, self.head.direction, self.second_element)

            vector = get_vector(self.head.direction)
            self.head.x += vector[0]
            self.head.y += vector[1]

            self.head.next_element = new_element

        temp = self.head
        while True:
            if temp.next_element.next_element is None:
                if temp.distance_to_next_element == 1:
                    temp.next_element = None
                else:
                    vector = get_vector(temp.direction)
                    temp.next_element.x += vector[0]
                    temp.next_element.y += vector[1]
                break
            else:
                temp = temp.next_element


class Element:
    def __init__(self, x: int, y: int, direction: int, next_element=None):
        self.x = x
        self.y = y
        self._direction = direction
        self.next_element = next_element

    def turn_right(self) -> None:
        """
        Поворачиает звено змейки направо
        :return:
        """
        self._direction += 1

    def turn_left(self) -> None:
        """
        Поворачиает звено змейки налево
        :return:
        """
        self._direction -= 1

    @property
    def direction(self) -> int:
        return self._direction % 4

    @property
    def distance_to_next_element(self) -> int:
        """
        Возвращает расстояние до следующего звена
        :return: Расстояние до следующего звена
        """
        if self.next_element is None:
            return 0

        delta_x = abs(self.x-1 - self.next_element.x)
        delta_y = abs(self.y-1 - self.next_element.y)
        return delta_x + delta_y
