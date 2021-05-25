# [pySnake] Соревновательная площадка 

Данный проект посвящён созданию соревновательной площадке, главной игрой который является змейка. Пользователи могут участвовать в многопользовательских змеиных баталиях, управляя своей змейкой с помощью кода. Необходимо будет написать алгоритм на языке Python, который сможет справиться с препятствиями, с врагами, с поеданием яблок, и, самое главное, с собой!

---
## Зависимости
В проекте были использованы сторонние пакеты такие как 
**flask**(1.1.2), **pymongo**(3.11.3) и **pyyaml**(5.4.1).

Для установки зависимостей введите команду `pip3 install -r requirements.txt`


---
## Информация о проекте

Проект делали студенты СФУ ИКИТ группы КИ20-17/2Б:
- [Черных Никита](https://github.com/Chevik08) _(Делал саму змейку)_
- [Терентьев Андрей](https://github.com/qpexlegendary) _(Занимался backend разработкой)_
- [Бочкарев Александр](https://github.com/AlexandarViWE) _(Занимался frontend разработкой)_

В проекте была использована библиотека [CodeMirror](https://codemirror.net/) для подстветки синтаксиса.

---

## Команды для управления змейкой

**check_forward()** - Проверить объекты впереди

    Возвращает число:
    0 - Спереди пусто
    1 - Спереди твердый объект
    2 - Спереди яблоко

**check_right()** - Проверить объекты справа

    Возвращает число:
    0 - Справа пусто
    1 - Справа твердый объект
    2 - Справа яблоко

**check_left()** - Проверить объекты слева

    Возвращает число:
    0 - Слева пусто
    1 - Слева твердый объект
    2 - Сслева яблоко

**put_memory(address: str, value: int)** - Заносит число *value* по адресу *address*
    
    Возвращает bool в зависимости от успеха. Возвращает False, если value не является числом, либо превышено количество переменных.

**get_memory(address: str)** - Получает число из адреса *address*
    
    Возвращает указанное число из памяти, либо вернет None в случае его отсутствия

**contains_memory(address: str)** - Проверка наличия значения по адресу address

    Возвращает True в случае, если адрес занят. Иначе False

**turn_right()** - Повернуть направо

**turn_left()** - Повернуть налево
