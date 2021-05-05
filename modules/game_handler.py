import time
from threading import Thread
import asyncio
from logging import Logger
from database import db_get_ended_games


class GameHandler(Thread):
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def run(self) -> None:
        self.logger.info("Запуск обработчика игр")
        while True:
            games = db_get_ended_games()

            for game_id in games:
                asyncio.run(self.handle(game_id))
            time.sleep(5)

    async def handle(self, game_id: str):
        # TODO: Обработка игр
        pass
