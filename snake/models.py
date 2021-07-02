import os
import json
import time

from main import mysql as db
from user import models as um
from snake import constants as uc


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
        return (self.start_time < time.time() < self.end_time) or self.status == uc.NOT_STARTED

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

    def end(self, best_player: um.User):
        with db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO winners (game, user) VALUES ({self.id}, {best_player.id});
                """)

            players = self.players
            for player in players:
                player.end_game(best_player.id == player.id)


def get_by_id(game_id: int) -> GameModel or None:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT * FROM games WHERE id = {game_id} LIMIT 1;
        """)
        result = cursor.fetchone()
        return None if result is None else GameModel(result)
