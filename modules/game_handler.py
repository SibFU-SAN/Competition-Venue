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

            asyncio.run(self.handle(games))
            time.sleep(5)

    async def handle(self, games: list):
        # TODO: Обработка игр
        pass
