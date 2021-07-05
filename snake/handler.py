import time
from threading import Thread
import asyncio
from logging import Logger
from app.game import models as gm, constants as gc
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
            time_end = int(time.time())
            games = gm.get_ended_games(time_end)

            for game in games:
                asyncio.run(self.handle(game))
            time.sleep(5)

    async def handle(self, game: gm.GameModel):
        log = self.logger.getChild(game.id)
        log.info("Запуск обработки игры")

        if len(game.players) == 0:
            log.info("В игре не участвовали пользователи. Удаляю игру из базы данных")
            game.remove()
            return

        try:
            start(game)
        except Exception as ex:
            log.exception("Произошла ошибка при обработке игры", exc_info=ex)
            game.handled_with_errors()
        else:
            log.info("Обработка игры успешно завершена")


def start(game_data: gm.GameModel):
    game = s.Game(game_data, 50 * 2, 50)

    scripts = dict()
    for player in game.players:
        script = game_data.read_script(player)
        scripts[player] = script

    winner_id = int(game.start(scripts))
    winner, *_ = [player for player in game.players if player.id == winner_id]

    game_data.save_demo(game.world.demo)
    game_data.end(winner)
