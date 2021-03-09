import re
import hashlib
import pymongo

db = pymongo.MongoClient("localhost")['test']


def generate_token(login: str, password: str) -> str:
    return hashlib.md5("{}{}".format(login.lower(), password).encode()).hexdigest()


def db_is_exists_user(login: str) -> bool:
    """
    Проверить наличие пользователя в базе данных по логину
    :param login: Логин пользователя
    :return: Результат
    """
    result = db.get_collection('users').find_one({'login': re.compile(f'^{login}$', re.IGNORECASE)})
    return result is not None


def db_create_user(login: str, password: str) -> str:
    """
    Создание пользователя
    :param login: Логин
    :param password: Пароль
    :return: Токен
    """
    if db_is_exists_user(login):
        raise RegistrationError(23, 'Пользователь уже существует')
    token = generate_token(login, password)
    db.get_collection('users').insert_one({
        '_id': hashlib.md5(login.lower().encode()).hexdigest(),
        'login': login,
        'password': hashlib.sha1(password.encode()).hexdigest(),
        'group': 0,
        'token': token
    })
    return token


def db_auth(login: str, password: str) -> dict:
    """
    Авторизация
    :param login: Логин
    :param password: Пароль
    :return: Данные о пользователе
    """
    token = generate_token(login, password)
    data = db.get_collection('users').find_one({'token': token}, {'token': 1})

    if data is None:
        raise LoginError(31, "Неверный логин и пароль")
    return data


def db_get_user_data(token: str) -> dict:
    """
    Получение данных пользователя
    :param token: Токен
    :return: Данные пользователя
    """
    data = db.get_collection('users').find_one({'token': token}, {'password': 0, 'token': 0})
    if data is None:
        raise LoginError(32, "Введен неверный токен")
    return data


class BaseResponseError(Exception):
    def __init__(self, error_id: int, message: str, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.error_id = error_id
        self.message = message


class RegistrationError(BaseResponseError):
    pass


class LoginError(BaseResponseError):
    pass
