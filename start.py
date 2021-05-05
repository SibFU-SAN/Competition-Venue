from snake_folder import snake_controls, multiplayer
import os


def start(game_hash: str):
    players_hash = []
    count = 0
    snake = [[[4, 3], [5, 3]], [[4, 8], [5, 8]]]
    names = os.listdir("snake_folder/Resources\\Scripts")
    """game_info = database.db_get_game_data(game_hash)
    map_size = game_info['map_size']"""
    for i in names:
        if str(i) == game_hash:
            players = os.listdir(f"snake_folder/Resources\\Scripts\\{i}")
            for pl in players:
                players_hash.append(players[count][0:-4])
                with open(f"snake_folder/Resources\\Scripts\\{i}\\{pl}", "r", encoding="utf-8") as file:
                    code = file.read()
                snake_controls.code = code
                snake_controls.snake_position = snake[count]
                snake_controls.apples_arr = [[7, 2], [2, 2], [2, 7], [7, 7]]
                snake_controls.direction = 1
                """snake_controls.height = int(sqrt(map_size))
                snake_controls.weight = int(sqrt(map_size))
                snake_controls.rad = game_info["view_distance"]"""
                snake_controls.height = 10
                snake_controls.weight = 10
                snake_controls.rad = 3
                snake_controls.server_info = []
                snake_controls.map_1 = snake_controls.start_options(
                    snake_controls.apples_arr)
                snake_controls.wall = snake_controls.map_gen()
                snake_controls.final()
                count += 1

            with open("snake_folder\\single_user.txt", "r", encoding="utf-8") as file:
                scripts = file.read()
                scripts = scripts[0:-1]
                scripts = eval(scripts)
            """Вычисление длительности игры(тест и вообще не нужно)"""
            max_script = 0
            info = []
            for j in range(len(scripts)):
                if max_script < len(scripts[j]):
                    max_script = len(scripts[j])
                info.append(scripts[j])
            multiplayer.players_number = len(players)
            multiplayer.iteration_count = max_script
            multiplayer.game_hash = game_hash
            """multiplayer.height = int(sqrt(map_size))
            multiplayer.weight = int(sqrt(map_size))"""
            multiplayer.height = 10
            multiplayer.weight = 10
            multiplayer.apples = snake_controls.apples_arr
            multiplayer.all_info = info
            multiplayer.hash_ = players_hash
            multiplayer.multi(multiplayer.all_info, snake_controls.map_1,
                              multiplayer.players_number,
                              multiplayer.iteration_count, multiplayer.hash_)
