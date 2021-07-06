import os
import json
import time

from . import constants as g
from app.database import db
import app.user as u


class GameModel:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.start_time = data[2]
        self.end_time = data[3]
        self.period = data[4]
        self.owner = u.get_by_id(data[5])
        self.__status = data[6]
        self.private = data[7]
        self.mode = data[8]
        self.settings = json.JSONEncoder().encode(data[9])
        self.__cached_players = None

    @property
    def status(self) -> int:
        if self.__status == g.NOT_STARTED and time.time() > self.start_time:
            return g.STARTED
        return self.__status

    @property
    def count_players(self) -> int:
        return len(self.players)

    @property
    def players(self) -> list:
        if self.__cached_players is None:
            with db.connect() as conn, conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT game, user FROM players WHERE game = {self.id};
                """)
                data = cursor.fetchall()
            self.__cached_players = [u.get_by_id(obj[1]) for obj in data]
        return self.__cached_players

    @property
    def winner(self) -> u.User or None:
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT game, user FROM winners WHERE game = {self.id} LIMIT 1;
            """)
            result = cursor.fetchone()
            return None if result is None else u.get_by_id(result[1])

    @property
    def can_play(self):
        return (self.start_time < time.time() < self.end_time) or self.__status == g.NOT_STARTED

    @property
    def left_time(self) -> int:
        t = self.end_time - int(time.time())
        return t if t > 0 else 0

    @property
    def demo(self) -> str or None:
        if not os.path.exists(f"./resources/demos/{self.id}"):
            return None
        with open(f'./resources/demos/{self.id}', 'r') as file:
            return file.read()

    @property
    def has_demo(self):
        return os.path.exists(f"./resources/demos/{self.id}")

    def save_demo(self, demo):
        with open(f'./resources/demos/{self.id}', 'w') as file:
            file.write(json.JSONEncoder().encode(demo))

    def save_script(self, user: u.User, script: str):
        if not os.path.exists(f"./resources/scripts/{self.id}"):
            os.mkdir(f"./resources/scripts/{self.id}")

        with open(f'./resources/scripts/{self.id}/{user.id}.py', 'w', encoding="utf-8") as file:
            file.write(script)

    def read_script(self, user: u.User) -> str:
        if not os.path.exists(f"./resources/scripts/{self.id}"):
            return ""
        if not os.path.exists(f"./resources/scripts/{self.id}/{user.id}.py"):
            return ""

        with open(f'./resources/scripts/{self.id}/{user.id}.py', 'r', encoding="utf-8") as file:
            return file.read()

    def end(self, best_player: u.User):
        with db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO winners (game, user) VALUES ({self.id}, {best_player.id});
                """)
                conn.commit()

            players = self.players
            for player in players:
                player.end_game(best_player.id == player.id)

            with conn.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE games SET status = {g.HANDLED}
                    WHERE id = {self.id} LIMIT 1;
                """)
                conn.commit()

    def close(self):
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                UPDATE games SET status = {g.CANCELLED_BY_OWNER} WHERE id = {self.id} LIMIT 1;
            """)
            conn.commit()

    def contains_player(self, user: u.User) -> bool:
        game = get_active_game(user)
        return False if game is None else (game.id == self.id)

    def add_player(self, user: u.User):
        if get_active_game(user) is not None:
            raise GameError('Вы уже участвуете в другой игре')
        if self.__status != g.NOT_STARTED:
            raise GameError('Игра уже окончена')

        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO players (game, user) VALUES ({self.id}, {user.id});
            """)
            conn.commit()

    def remove(self):
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM games WHERE id = {self.id} LIMIT 1;
            """)
            conn.commit()

    def handled_with_errors(self):
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                UPDATE games SET status = {g.ENDED_WITH_ERRORS} WHERE id = {self.id} LIMIT 1;
            """)
            conn.commit()


class GameError(Exception):
    def __init__(self, message: str):
        self.message = message


def get_by_id(game_id: int) -> GameModel or None:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT * FROM games WHERE id = {game_id} LIMIT 1;
        """)
        result = cursor.fetchone()
        return None if result is None else GameModel(result)


def get_games(count: int = 7, status: int = g.NOT_STARTED) -> list:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT * FROM games WHERE private = false AND status = {status} ORDER BY id DESC;
        """ + (f"LIMIT {count}" if count > 0 else ""))
        return [GameModel(data) for data in cursor.fetchall()]


def get_user_games(user: u.User, count: int = 7) -> list:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT games.* FROM games JOIN players 
            WHERE players.game = games.id AND players.user = {user.id}
            ORDER BY games.id DESC LIMIT {count};
        """)
        return [GameModel(data) for data in cursor.fetchall()]


def get_ended_games(time_now: int, mark_as_handling: bool = True) -> list:
    with db.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                        SELECT * FROM games 
                        WHERE status = {g.NOT_STARTED} AND end_time <= {time_now};
                    """)
            result = [GameModel(data) for data in cursor.fetchall()]

        if mark_as_handling:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE games SET status = {g.HANDLING}
                    WHERE status = {g.NOT_STARTED} AND end_time <= {time_now};
                """)
                conn.commit()
        return result


def get_active_game(user: u.User) -> GameModel or None:
    if user.cached_game is not None:
        return user.cached_game

    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT game FROM players WHERE user = {user.id} ORDER BY id DESC LIMIT 1;
        """)
        result = cursor.fetchone()
        if result is None:
            return None
        game = get_by_id(result[0])
        if game is None:
            return None
        user.cached_game = game if game.can_play else None
        return user.cached_game


def create(owner: u.User, add_self: bool, name: str, period: int, start_time: int,
           private: bool, mode: int, view_distance: int, **kwargs) -> GameModel:

    end_time = start_time + period * 60
    settings = kwargs
    settings['view_distance'] = view_distance
    serialized_settings = json.JSONEncoder().encode(settings)

    with db.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO games (name, start_time, end_time, period, owner, private, mode, settings) 
                VALUES (%s, {start_time}, {end_time}, {period}, {owner.id}, {private}, {mode}, %s)
            """, [name, serialized_settings])
            conn.commit()

        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT * FROM games WHERE
                 name = %s AND
                  start_time = {start_time} AND
                  owner = {owner.id}
                  ORDER BY id DESC LIMIT 1;
            """)
            game_data = cursor.fetchone()

            if game_data is None:
                raise GameError('Произошла неизвестная ошибка при создании и игры')

            game = GameModel(game_data)
            if add_self:
                game.add_player(owner)
            return game
