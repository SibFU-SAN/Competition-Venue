# Соревновательная площадка

Данный проект посвящён созданию соревновательной площадке, главной игрой который является змейка. Пользователи могут участвовать в многопользовательских змеиных баталиях, управляя своей змейкой с помощью кода. Необходимо будет написать алгоритм на языке Python, который сможет справиться с препятствиями, с врагами, с поеданием яблок, и, самое главное, с собой!

---
## Зависимости
В проекте были использованы сторонние пакеты такие как 
**flask**(1.1.2), **pymongo**(3.11.3) и **pyyaml**(5.4.1).

Для установки зависимостей введите команду `pip3 install -r requirements.txt`


---
### Информация о проекте

Проект делали студенты СФУ ИКИТ группы КИ20-17/2Б:
- [Черных Никита](https://github.com/Chevik08) _(Делал саму змейку)_
- [Терентьев Андрей](https://github.com/qpexlegendary) _(Занимался backend разработкой)_
- [Бочкарев Александр](https://github.com/AlexandarViWE) _(Занимался frontend разработкой)_
 ________________________________________
### Принцип работы блока snake
Как только игрок заканчивает написание кода и отправляет его, то он заносится в папку как snake_folder\Resources\Scripts\”Хеш_игры”\”Хеш_игрока”. Как только скрипты всех игроков будут отправлены, запускается метод start, который получает на вход хеш игры. По этому хешу он выбирает из папки Scripts нужный файл со скриптами всех игроков и поочерёдно обрабатывает их в модуле snake_controls. Результат обработки модуля заносится в файл single_user.txt. После окончания обработки каждого скрипта отдельно, запускается модуль multiplayer, который обрабатывает результат запуска всех корректных скриптов одновременно. Результат заносится в snake_folder\Resources\Demos\”Хеш_игры”. На этом заканчивается работа метода start и далее результат визуализируется на сайте для пользователей.
За всю логику, обработку коллизий, увеличение размера и передвижение непосредственно змейки отвечает модуль snake_game
 ________________________________________
#### Команды для управления змейкой
move_left() - поворот налево
move_right() - поворот направо
move_up() - поворот вверх
move_down() - поворот вниз
move() - движение в том направлении, в котором двигались до этого
wall_is_left(rad=1) - проверка на стену слева на расстоянии rad, возвращает 0 или 1
wall_is_right(rad=1) - проверка на стену справа на расстоянии rad, возвращает 0 или 1
wall_is_up(rad=1) - проверка на стену сверху на расстоянии rad, возвращает 0 или 1
wall_is_down(rad=1) - проверка на стену снизу на расстоянии rad, возвращает 0 или 1
food(rad=1) - проверка на еду в области видимости, возвращает 0 или 1
direction_right() - проверка на то, в каком движении направляется змейка, возвращает 0 или 1
direction_left() - проверка на то, в каком движении направляется змейка, возвращает 0 или 1
direction_up() - проверка на то, в каком движении направляется змейка, возвращает 0 или 1
direction_down() - проверка на то, в каком движении направляется змейка, возвращает 0 или 1

rad - радиус обзора змейки, заданный пользователем
