from snake.snake import Map
import copy
import json
import uuid


def start(map_height, map_weight):

    """with open("single_user.txt", "r", encoding="utf-8") as multi:
        players = multi.read()
    players = players[0:-1]
    players = eval(players)
    for pl in range(len(players)):
        all_info.append(players[pl])"""

    return map1, players_number, iteration_count, all_info, apples,\
        map_height, map_weight


def head_to_tail(info, pl_snake, num, ite, warn, except_list):
    for non_pl_snake in range(num):
        if pl_snake != non_pl_snake and info[pl_snake][ite] != ['stop'] \
                and info[non_pl_snake] not in except_list:
            if info[pl_snake][ite][0] == info[non_pl_snake][ite][1:]:
                info[pl_snake][ite] = ['stop']
                warn += 1
            elif info[pl_snake][ite][1:][0] == info[non_pl_snake][ite][0]:
                info[non_pl_snake][ite] = ['stop']
                warn += 1

            if warn > 0:
                except_list.append(info[non_pl_snake])
                break


def head_to_head(info, pl_snake, num, ite, warn, except_list):
    for non_pl_snake in range(num):
        if pl_snake != non_pl_snake and info[pl_snake][ite] != ['stop'] \
                and info[non_pl_snake] not in except_list:
            if info[pl_snake][ite][0] == info[non_pl_snake][ite][0]:
                warn += 1

            if warn > 0:
                info[pl_snake][ite] = ['stop']
                info[non_pl_snake][ite] = ['stop']
                except_list.append(info[non_pl_snake])
                except_list.append(info[pl_snake])
                break


def multi(info, map_1, num, it_count, _hash):
    user_id = []
    except_list = []
    warn = 0
    map_before = copy.deepcopy(map_1)
    players_info = []
    list_for_sasha = {
        "apples": [],
        "snakes": {

        }
    }

    first_scene = {
        'players': {

        },
        'gameSettings': {
            'height': height,
            'weight': weight
        },
        "frame": []
    }
    for pl_snake in range(num):
        _id = uuid.uuid4()
        user_id.append(int(str(int(_id))[0:8]))
        first_scene['players'][f"{user_id[pl_snake]}"] = _hash[pl_snake]
        for ite in range(it_count):
            if info[pl_snake] not in except_list:
                if 'stop' in info[pl_snake][ite]:
                    except_list.append(info[pl_snake])

                    cleaner = len(info[pl_snake][ite-1])
                else:
                    cleaner = len(info[pl_snake][ite])

                head_to_tail(info, pl_snake, num, ite, warn, except_list)
                head_to_head(info, pl_snake, num, ite, warn, except_list)

                for segments in range(cleaner):

                    if info[pl_snake] not in except_list:
                        if segments == 0:
                            map_1[info[pl_snake][ite][segments][0]][
                                info[pl_snake][ite][segments][1]] = '🐸'
                        else:
                            map_1[info[pl_snake][ite][segments][0]][
                                info[pl_snake][ite][segments][1]] = '◻'
                    else:
                        for i in range(len(info[pl_snake])):
                            if i != len(info[pl_snake])-1 and info[pl_snake][
                               i] != ['stop']:
                                if segments == 0:
                                    map_1[info[pl_snake][i][segments][0]][
                                        info[pl_snake][i]
                                        [segments][1]] = ' '
                                else:
                                    map_1[info[pl_snake][i][segments][0]][
                                        info[pl_snake][i]
                                        [segments][1]] = ' '

            if info[pl_snake][ite] == ['stop']:
                players_info.append(info[pl_snake][ite])
                break
            else:
                players_info.append(info[pl_snake][ite])
        if ['stop'] not in players_info:
            players_info.append(['stop'])

        map_1 = copy.deepcopy(map_before)

    except_list.clear()
    start_ = 0
    new_players_info = []

    """Рвзделение на отдельные списки под каждого игрока"""
    for a in range(len(players_info)):
        if players_info[a] == ['stop']:
            new_players_info.append(players_info[start_:a+1])
            start_ = a+1

    """Обрезание пути змейки"""
    for i in range(len(info)):
        for j in range(len(info[i])):
            if info[i][j] == ['stop']:
                del info[i][j]
                break

    """Запись в Саша-файл"""
    for it in range(it_count):
        for us in range(len(new_players_info)):
            if not it >= len(new_players_info[us]):
                if new_players_info[us] not in except_list:
                    list_for_sasha['snakes'][
                        f'{copy.deepcopy(user_id[us])}']\
                        = copy.deepcopy(new_players_info[us][it])
                    del_apples = []
                    for app in range(len(apples)):
                        if new_players_info[us][it][0] == apples[app]:
                            del_apples.append(app)
                    for i in range(len(del_apples)):
                        del apples[i]
                    list_for_sasha['apples'] = copy.deepcopy(apples)
                else:
                    continue
            else:
                except_list.append(new_players_info[us])
        first_scene['frame'].append(copy.deepcopy(list_for_sasha))
    with open(f"../resources/demos/{game_hash}", "a+", encoding="utf-8") as file:
        json.dump(first_scene, file, indent=2)


if __name__ == '__main__':
    game_hash = ''
    hash_ = []
    all_info = []
    height = 0
    weight = 0
    apples = []
    map1 = Map(height, weight, apples).map()
    players_number = 0
    iteration_count = 0
