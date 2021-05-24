from json import encoder
from random import randint, choice

VECTOR_UP = (0, 1)
VECTOR_DOWN = (0, -1)
VECTOR_RIGHT = (1, 0)
VECTOR_LEFT = (-1, 0)
vectors = [VECTOR_UP, VECTOR_RIGHT, VECTOR_DOWN, VECTOR_LEFT]


def get_direction_vector(n: int) -> tuple:
    return vectors[n % 4]


def is_collide_el(x: int, y: int, p1, p2) -> bool:
    x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
    y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)
    return (x_min <= x <= x_max) and (y_min <= y <= y_max)


def is_collided(world, x: int, y: int) -> bool:
    for snake in world.snakes:
        if not snake.alive:
            continue
        el = snake.head
        while el.next is not None:
            if is_collide_el(x, y, el, el.next):
                return True
            el = el.next
    return False


def get_distance(el, target) -> int:
    return abs(el.x - target.x) + abs(el.y - target.y)


class World:
    def __init__(self, x_max: int, y_max: int):
        self.x_max = x_max
        self.y_max = y_max
        self.snakes = list()
        self.apples = set()
        self.demo = {
            'players': list(),
            'gameSettings': {
                'height': y_max,
                'weight': x_max,
            },
            'frames': [],
        }
        self.tick = 0

    def is_out(self, x: int, y: int):
        return x not in range(0, self.x_max) or y not in range(0, self.y_max)

    @property
    def get_spawn_location(self) -> tuple:
        x_min, y_min = 3, 3
        x_max, y_max = self.x_max - 3, self.y_max - 3

        left = ((x_min, y_min), (x_min, y_max))
        right = ((x_max, y_min), (x_max, y_max))
        up = ((x_min, y_max), (x_max, y_max))
        down = ((x_min, y_min), (x_max, y_min))

        line = choice([left, right, up, down])

        if line == down:
            return x_min + randint(1, x_max - 1), y_min, 2
        if line == up:
            return x_min + randint(1, x_max - 1), y_max, 0
        if line == left:
            return x_min, y_min + randint(1, x_max - 1), 3
        if line == right:
            return x_max, y_min + randint(1, x_max - 1), 1

    def spawn(self, uid: str):
        while True:
            loc = self.get_spawn_location
            for snake in self.snakes:
                if snake.head.x == loc[0] and snake.head.y == loc[1]:
                    continue

            snake = Snake(uid, loc[0], loc[1], 2 + loc[2], self)
            self.snakes.append(snake)
            break

    def spawn_apples(self):
        if self.tick % 10 != 0:
            return

        for _ in range(3):
            while True:
                x, y = randint(0, self.x_max - 1), randint(0, self.y_max)
                if is_collided(self, x, y):
                    continue
                self.apples.add((x, y))
                break

    def handle(self) -> bool:
        # TODO: Выполнение пользовательских скриптов
        for snake in self.snakes:
            snake.head.turn_left()

        frame = {
            'snakes': dict()
        }
        # Обработка движений
        damaged = self.tick % 10 == 0
        for snake in self.snakes:
            if not snake.alive:
                continue
            eaten = snake.head.check_apple_collide(self)
            snake.move(damaged, eaten)
            if eaten:
                snake.score += 1

        # Обработка коллизии
        for snake in self.snakes:
            if not snake.alive:
                continue
            if snake.is_collided():
                snake.alive = False

        # Запись в демку
        tmp = list()
        for snake in self.snakes:
            if not snake.alive:
                continue
            el = snake.head
            while el is not None:
                tmp.append((el.x, el.y))
                el = el.next
            frame['snakes'][snake.id] = tmp
        frame['apples'] = tuple([apple for apple in self.apples])
        self.demo['frames'].append(frame)

        # Завершение игры
        alive_snakes = 0
        for snake in self.snakes:
            if snake.alive:
                alive_snakes += 1
        if alive_snakes == 0:
            return True

        self.spawn_apples()
        self.tick += 1
        return False


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.next = None

    def get_next_el_vector(self) -> tuple or None:
        if self.next is None:
            return None

        x, y = 0, 0
        if self.x != self.next.x:
            x = 1 if self.x > self.next.x else 0
        if self.y != self.next.y:
            y = 1 if self.y > self.next.y else 0
        return x, y


class Head(Point):
    def __init__(self, x: int, y: int, direction: int):
        super().__init__(x, y)
        self.direction = direction

    def turn_right(self):
        self.direction += 1

    def turn_left(self):
        self.direction -= 1

    def check_apple_collide(self, world: World) -> bool:
        vec = get_direction_vector(self.direction)
        pos = (self.x + vec[0], self.y + vec[1])

        if pos in world.apples:
            world.apples.remove(pos)
            return True
        return False


class Snake:
    def __init__(self, uid: str, x_spawn: int, y_spawn: int, direction: int, world: World):
        self.id = uid
        self.head = Head(x_spawn, y_spawn, direction)
        self.alive = True
        self.world = world
        self.score = 0

        vector = get_direction_vector(direction)
        self.head.next = Point(vector[0] * -3, vector[1] * -3)

    def is_collided(self) -> bool:
        x, y = self.head.x, self.head.y
        if self.world.is_out(x, y):
            return True

        for snake in self.world.snakes:
            if not snake.alive:
                continue
            el = snake.head
            while el.next is not None:
                if is_collide_el(x, y, el, el.next):
                    if el != self.head:
                        return True
                el = el.next
        return False

    def move(self, damaged: bool, eaten: bool):
        head_direction = get_direction_vector(self.head.direction)
        next_direction = self.head.get_next_el_vector()

        # Голова
        if head_direction != next_direction:
            new_point = Point(self.head.x, self.head.y)
            new_point.next = self.head.next
        self.head.x += head_direction[0]
        self.head.y += head_direction[1]

        # Хвост
        for i in range(2 if damaged and not eaten else 1):
            pre_last = self.head
            last = self.head.next
            while (last.next is not None) and (last.next.next is not None):
                pre_last = pre_last.next
                last = last.next
            if get_distance(pre_last, last) < 2:
                pre_last.next = None
            else:
                if eaten and i == 0:
                    continue
                direction = pre_last.get_next_el_vector()
                last.x += direction[0]
                last.y += direction[1]

        # Условие на смерть от голода
        if self.head.next is None:
            self.alive = False


class Game:
    def __init__(self, game_id: str, players: list, x_max: int, y_max: int):
        self.game_id = game_id
        self.players = players

        self.world = World(x_max, y_max)

    def start(self):
        # Спавн игроков
        for player in self.players:
            self.world.spawn(player)

        # Обработка игры
        while True:
            if self.world.handle():
                break

        # TODO: Подведение итогов


if __name__ == '__main__':
    game = Game("123", ['test1'], 10, 10)
    game.start()
    print(encoder.JSONEncoder().encode(game.world.demo))
    print(game.world.tick)
