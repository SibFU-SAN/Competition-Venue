import os
import json
import time

from main import mysql as db
from app.user import models as um
from app.game import constants as gc


class GameModel:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.period = data['period']
        self.owner = um.get_by_id(data['owner'])
        self.status = data['status']
        self.private = data['private']
        self.settings = json.JSONEncoder().encode(data['settings'])

    @property
    def players(self) -> list:
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT game, user FROM players WHERE game = {self.id};
            """)
            data = cursor.fetchall()
            return [um.get_by_id(obj['user']) for obj in data]

    @property
    def winner(self) -> um.User or None:
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT game, user FROM winners WHERE game = {self.id} LIMIT 1;
            """)
            result = cursor.fetchone()
            return None if result is None else um.get_by_id(result['user'])

    @property
    def can_play(self):
        return (self.start_time < time.time() < self.end_time) or self.status == gc.NOT_STARTED

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

    def save_demo(self, demo):
        with open(f'./resources/demos/{self.id}', 'w') as file:
            file.write(json.JSONEncoder().encode(demo))

    def save_script(self, user: um.User, script: str):
        if not os.path.exists(f"./resources/scripts/{self.id}"):
            os.mkdir(f"./resources/scripts/{self.id}")

        with open(f'./resources/scripts/{self.id}/{user.id}.py', 'w', encoding="utf-8") as file:
            file.write(script)

    def read_script(self, user: um.User) -> str:
        if not os.path.exists(f"./resources/scripts/{self.id}"):
            return ""
        if not os.path.exists(f"./resources/scripts/{self.id}/{user.id}.py"):
            return ""

        with open(f'./resources/scripts/{self.id}/{user.id}.py', 'r', encoding="utf-8") as file:
            return file.read()

    def end(self, best_player: um.User, time_end: int):
        with db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO winners (game, user) VALUES ({self.id}, {best_player.id});
                """)

            players = self.players
            for player in players:
                player.end_game(best_player.id == player.id)

            with conn.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE games SET status = {gc.HANDLED}
                    WHERE status = {gc.NOT_STARTED} AND end_time <= {time_end};
                """)

    def close(self):
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                UPDATE games SET status = {gc.CANCELLED_BY_OWNER} WHERE id = {self.id} LIMIT 1;
            """)

    def contains_player(self, user: um.User) -> bool:
        game = user.active_game
        return False if game is None else (game.id == self.id)

    def add_player(self, user: um.User):
        if user.active_game is not None:
            raise GameError('Вы уже участвуете в другой игре')
        if self.status != gc.NOT_STARTED:
            raise GameError('Игра уже окончена')

        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO players (game, user) VALUES ({self.id}, {user.id});
            """)

    def remove(self):
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM games WHERE id = {self.id} LIMIT 1;
            """)


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


def get_games(count: int = 7, status: int = gc.NOT_STARTED) -> list:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT * FROM games WHERE private = false AND status = {status} ORDER BY id DESC;
        """ + (f"LIMIT {count}" if count > 0 else ""))
        return [GameModel(data) for data in cursor.fetchall()]


def get_user_games(user: um.User, count: int = 7) -> list:
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
                        WHERE status = {gc.NOT_STARTED} AND end_time <= {time_now};
                    """)
            result = [GameModel(data) for data in cursor.fetchall()]

        if mark_as_handling:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE games SET status = {gc.HANDLING}
                    WHERE status = {gc.NOT_STARTED} AND end_time <= {time_now};
                """)
        return result


def create(owner: um.User, add_self: bool, name: str, period: int, start_time: int,
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
