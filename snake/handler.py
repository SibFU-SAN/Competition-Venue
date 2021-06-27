import time
from threading import Thread
import asyncio
from logging import Logger
from modules import database, account_methods
from modules.database import db_get_ended_games, db_get_game_data, db_remove_game
from snake import game as s


exec_options = {"__cached__": None, "__doc__": None, "__file__": None,
                "__name__": None, "__loader__": None, "__package__": None,
                "__spec__": None, "print": None, "exec": None,
                "eval": None}


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
        log = self.logger.getChild(game_id)
        log.info("Запуск обработки игры")

        game_data = db_get_game_data(game_id)
        if len(game_data['players']) == 0:
            log.info("В игре не участвовали пользователи. Удаляю игру из базы данных")
            db_remove_game(game_id)
            return

        try:
            start(game_id)
        except Exception as ex:
            log.exception("Произошла ошибка при обработке игры", exc_info=ex)
        else:
            log.info("Обработка игры успешно завершена")


def start(game_hash: str):
    game_data = database.db_get_game_data(game_hash)
    game = s.Game(game_hash, game_data['players'], game_data['map_size'] * 2,
                  game_data['map_size'], game_data['view_distance'])

    scripts = dict()
    for player in game.players:
        script = account_methods.read_script(game_hash, player)
        scripts[player] = script

    game.start(scripts)
    account_methods.save_demo(game_hash, game.world.demo)
