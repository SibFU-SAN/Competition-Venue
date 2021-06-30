from json import encoder
from modules import game_starter, database
from random import randint, choice
from copy import deepcopy

VECTOR_UP = (0, 1)
VECTOR_DOWN = (0, -1)
VECTOR_RIGHT = (1, 0)
VECTOR_LEFT = (-1, 0)
vectors = [VECTOR_UP, VECTOR_RIGHT, VECTOR_DOWN, VECTOR_LEFT]


def check_distance(pos: tuple, target: tuple, distance: int):
    return (pos[0] - target[0])**2 + (pos[1] - target[2])**2 <= distance**2


def get_direction_vector(n: int) -> tuple:
    return vectors[n % 4]


def is_collide_el(x: int, y: int, p1, p2) -> bool:
    x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
    y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)
    return (x_min <= x <= x_max) and (y_min <= y <= y_max)


def is_collided(world, x: int, y: int) -> bool:
    if world.is_out(x, y):
        return True
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
    def __init__(self, x_max: int, y_max: int, view_distance: int, mode_id: int):
        self.x_max = x_max
        self.y_max = y_max
        self.snakes = list()
        self.apples = set()
        self.view_distance = view_distance
        self.emtpy_tick = 0
        self.mode_id = mode_id
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
            return randint(x_min + 1, x_max - 1), y_min, 2
        elif line == up:
            return randint(x_min + 1, x_max - 1), y_max, 0
        elif line == left:
            return x_min, randint(y_min + 1, y_max - 1), 3
        elif line == right:
            return x_max, randint(y_min + 1, y_max - 1), 1

    def spawn(self, uid: str):
        while True:
            loc = self.get_spawn_location
            for snake in self.snakes:
                if snake.head.x == loc[0] and snake.head.y == loc[1]:
                    continue

            snake = Snake(uid, loc[0], loc[1], loc[2], self. mode_id)
            self.snakes.append(snake)
            self.demo['players'].append(snake.id)
            break

    def spawn_apples(self):
        if self.tick % 20 != 0 or len(self.apples) > self.x_max * self.y_max / 10:
            return

        for _ in range(int(self.x_max * self.y_max / 100)):
            while True:
                x, y = randint(0, self.x_max - 1), randint(0, self.y_max)
                if is_collided(self, x, y):
                    continue
                self.apples.add((x, y))
                break

    def handle(self, compiled_scripts) -> bool:
        # Запись в демку
        frame = {
            'snakes': dict()
        }

        # Выполнение пользовательских скриптов
        for snake in self.snakes:
            try:
                exec(compiled_scripts[snake.id], game_starter.exec_options, snake.get_controls())
            except Exception:
                pass

        # Отключение голода
        if self.mode_id == 1:
            damaged = self.tick % 20 == 19
        else:
            damaged = 1

        # Обработка движений
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

            temp = list()
            el = snake.head
            while el is not None:
                temp.append((el.x, el.y))
                el = el.next

            # Переспавн в яблоки
            if snake.is_collided():
                for snaky in self.snakes:
                    el = snaky.head
                    while el.next is not None:
                        tmp = deepcopy(el)
                        while (tmp.x != el.next.x) or (tmp.y != el.next.y):
                            if el.x > el.next.x:
                                tmp.x -= 1
                            elif el.x < el.next.x:
                                tmp.x += 1
                            elif el.y > el.next.y:
                                tmp.y -= 1
                            elif el.y < el.next.y:
                                tmp.y += 1
                            self.apples.add((tmp.x, tmp.y))
                        el = el.next
                    snake.alive = False

        # Запись демки
        for snake in self.snakes:
            if not snake.alive:
                continue
            tmp = list()
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
        if alive_snakes == 1:
            self.emtpy_tick += 1
        if self.emtpy_tick > 500:
            return True
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
            x = 1 if self.x < self.next.x else -1
        if self.y != self.next.y:
            y = 1 if self.y < self.next.y else -1
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
    def __init__(self, uid: str, x_spawn: int, y_spawn: int, direction: int, world: World,
                 mode_id: int):
        self.id = uid
        self.head = Head(x_spawn, y_spawn, direction + 2)
        self.alive = True
        self.world = world
        self.score = 0
        self.mode_id = mode_id
        self.memory = dict()

        vector = get_direction_vector(direction)
        self.head.next = Point(x_spawn + vector[0] * 2, y_spawn + vector[1] * 2)

    def get_controls(self) -> dict:
        return {
            'turn_right': lambda: self.head.turn_right(),
            'turn_left': lambda: self.head.turn_left(),
            'get_view_distance': lambda: self.world.view_distance,
            'check_forward': lambda: self.check_forward(),
            'check_right': lambda: self.check_right(),
            'check_left': lambda: self.check_left(),
            'put_memory': lambda address, value: self.put_memory(address, value),
            'get_memory': lambda address: self.get_memory(address),
            'contains_memory': lambda address: self.get_memory(address),
        }

    def put_memory(self, address: str, value: int) -> bool:
        if len(self.memory.values()) > 3:
            return False
        if type(value) != int:
            return False

        self.memory[address] = value
        return True

    def get_memory(self, address: str) -> int or None:
        if address in self.memory:
            return self.memory[address]
        return False

    def contains_memory(self, address: str) -> bool:
        return address in self.memory

    def check_forward(self) -> int:
        direction = get_direction_vector(self.head.direction)
        pos = (direction[0] + self.head.x, direction[1] + self.head.y)
        return 2 if pos in self.world.apples else (1 if is_collided(self.world, pos[0], pos[1]) else 0)

    def check_right(self) -> int:
        direction = get_direction_vector(self.head.direction + 1)
        pos = (direction[0] + self.head.x, direction[1] + self.head.y)
        return 2 if pos in self.world.apples else (1 if is_collided(self.world, pos[0], pos[1]) else 0)

    def check_left(self) -> int:
        direction = get_direction_vector(self.head.direction - 1)
        pos = (direction[0] + self.head.x, direction[1] + self.head.y)
        return 2 if pos in self.world.apples else (1 if is_collided(self.world, pos[0], pos[1]) else 0)

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

    def get_vision(self) -> dict:
        matrix = dict()
        x, y = self.head.x, self.head.y
        dv = self.world.view_distance

        for line in range(2 * dv + 1):
            matrix[line - dv] = \
                {col: is_collided(self.world, x - dv + line, y - dv + col) for col in range(2 * dv + 1)}
        for line in range(2 * dv + 1):
            for col in range(2 * dv + 1):
                matrix[line - dv][col - dv] = matrix[line - dv][col]
                del matrix[line - dv][col]
        return matrix

    def move(self, damaged: bool, eaten: bool):
        head_direction = get_direction_vector(self.head.direction + 2)
        next_direction = self.head.get_next_el_vector()

        # Голова
        if head_direction != next_direction:
            new_point = Point(self.head.x, self.head.y)
            new_point.next = self.head.next
            self.head.next = new_point
        self.head.x -= head_direction[0]
        self.head.y -= head_direction[1]

        # Хвост
        for i in range(2 if damaged and not eaten else 1):
            pre_last = self.head
            last = self.head.next
            while (last is not None) and (last.next is not None):
                pre_last = last
                last = last.next
            if get_distance(pre_last, last) < 1:
                pre_last.next = None
            else:
                if eaten and i == 0:
                    continue
                direction = pre_last.get_next_el_vector()

                #Убрать это при режиме без уменьшения хвоста
                if self.mode_id != 3:
                    last.x -= direction[0]
                    last.y -= direction[1]

        if self.head.next is None or get_distance(self.head, self.head.next) == 0:
            self.alive = False


class Game:
    def __init__(self, game_id: str, players: list, x_max: int, y_max: int, view_distance: int,
                 mode_id: int):
        self.game_id = game_id
        self.players = players
        self.mode_id = mode_id
        self.world = World(x_max, y_max, view_distance, mode_id)

    def start(self, scripts: dict):
        # Компилирование скриптов
        compiled_scripts = dict()
        for player in scripts.keys():
            try:
                compiled_scripts[player] = compile(scripts[player], "", "exec")
            except Exception:
                compiled_scripts[player] = compile("", "", "exec")

        # Спавн игроков
        for player in self.players:
            self.world.spawn(player)

        # Обработка игры
        while True:
            if self.world.handle(compiled_scripts):
                break

        # Подведение итогов
        scores = dict()
        for snake in self.world.snakes:
            scores[snake.id] = snake.score
        # database.db_end_game(self.game_id, scores)


if __name__ == '__main__':
    mode_id = 0
    players = [f"test{i}" for i in range(10)]
    game = Game("123", players, 120, 100, 5, mode_id)
    codes = ["""
if not contains_memory('right'):
    put_memory('right', 0)

if check_forward() == 1:
    if get_memory('right') == 1 and check_right() != 1:
        turn_right()
    elif check_left() != 1: 
        turn_left()
    else:
        turn_right()

if get_memory('right') == 1 and check_left() == 2 or check_right() == 1 and check_left() == 2:
    put_memory('right', 0)
    turn_left()
elif check_right() == 2:
    put_memory('right', 1)
    turn_right()
            """]

    scripts = dict()
    for player in players:
        scripts[player] = codes[randint(0, len(codes) - 1)]

    game.start(scripts)
    print(game.world.tick)
    with open(f"demo.json", 'w') as file:
        file.write(encoder.JSONEncoder().encode(game.world.demo))
