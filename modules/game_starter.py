from modules import database, account_methods
from snake_game import snake as s

exec_options = {"__cached__": None, "__doc__": None, "__file__": None,
                "__name__": None, "__loader__": None, "__package__": None,
                "__spec__": None, "print": None, "exec": None,
                "eval": None}


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
