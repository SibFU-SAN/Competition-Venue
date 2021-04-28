import time
from threading import Thread
from logging import Logger


class GameHandler(Thread):
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def run(self) -> None:
        self.logger.info("Запуск обработчика игр")
        while True:

            # TODO: Обработка игр
            time.sleep(5)
