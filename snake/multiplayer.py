from snake_game import Map
import copy
from visualisation import image

all_info = []
list_for_Sasha = []
with open("single_user.txt", "r", encoding="utf-8") as multi:
    players = multi.read()
players = players[0:-1]
players = eval(players)
print(players[0])
for pl in range(len(players)):
    all_info.append(players[pl])

"""Для примера"""
all_info.clear()

server_info1 = [[[4, 3], [3, 3]], [[5, 3], [4, 3]], ['stop']]
server_info2 = [[[4, 4], [4, 5]], [[4, 3], [4, 4]], [[4, 2], [4, 3]], ['stop']]
all_info.append(server_info1)
all_info.append(server_info2)
apples = [[7, 2], [2, 2], [2, 7], [7, 7]]
map1 = Map(10, 10, apples).map()
players_number = len(all_info)
iteration_count = 3


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


def multi(info, map_1, num, it_count):
    except_list = []
    warn = 0
    number = 1
    map_before = copy.deepcopy(map_1)
    for ite in range(it_count):
        for pl_snake in range(num):
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
                            if i != len(info[pl_snake])-1:
                                if segments == 0:
                                    map_1[info[pl_snake][i][segments][0]][
                                        info[pl_snake][i]
                                        [segments][1]] = ' '
                                else:
                                    map_1[info[pl_snake][i][segments][0]][
                                        info[pl_snake][i]
                                        [segments][1]] = ' '

        for j in range(10):
            print('   '.join(map_1[j]))
        print()

        image(number, map_1)
        number += 1
        with open("output_map.txt", 'a+', encoding='utf-8') as file_map:
            file_map.write(str(map_1))

        map_1 = copy.deepcopy(map_before)


if __name__ == '__main__':
    multi(all_info, map1, players_number, iteration_count)
    for i_ in range(len(all_info)):
        for j_ in range(len(all_info[i_])):
            if all_info[i_][j_] == ['stop']:
                list_for_Sasha.append(['stop'])
                break
            else:
                list_for_Sasha.append(all_info[i_][j_])
    with open("output.txt", 'w', encoding='utf-8') as file:
        file.write(str(list_for_Sasha))
