import re
import hashlib
import pymongo


def connect(host: str, port: str, base: str, auth: bool, user: str, password: str, auth_base: str):
    global db

    db = pymongo.MongoClient(f"{host}:{port}")[base]
    if auth:
        db.authenticate(user, password, auth_base)


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


def db_check_token(token: str) -> bool:
    """
    Проверить наличие пользователя в базе данных по токену
    :param token: Токен пользователя
    :return: Результат
    """
    result = db.get_collection('users').find_one({'token': token})
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
        'token': token,
        'wins': 0,
        'played_games': 0,
        'best_score': 0,
    })
    return token


def db_auth(login: str, password: str) -> str:
    """
    Авторизация
    :param login: Логин
    :param password: Пароль
    :return: Токен
    """
    token = generate_token(login, password)
    data = db.get_collection('users').find_one({'token': token}, {'token': 1})

    if data is None:
        raise LoginError(31, "Неверный логин и пароль")
    return token


def db_get_user_data(key: str, by_token=True) -> dict:
    """
    Получение данных пользователя
    :param key: Значение
    :param by_token: Искать ли по токену? Иначе ищет по логину
    :return: Данные пользователя
    """
    data = db.get_collection('users').find_one({('token' if by_token else '_id'): key}, {'password': 0, 'token': 0})
    if data is None:
        raise LoginError(32, "Введен неверный токен")
    return data


def db_reset_password(token: str, new_password: str) -> dict:
    """
    Сброс пароля пользователем
    :param token: Токен
    :param new_password: Новый пароль пользователя
    :return: Данные с новым токеном
    """
    data = db.get_collection('users').find_one({'token': token}, {'login': 1})
    if data is None:
        raise ResetPasswordError(40, "Введен неверный токен")

    new_token = generate_token(data['login'], new_password)
    db.get_collection('users').update({'token': token}, {'$set': {
        'password': hashlib.sha1(new_password.encode()).hexdigest(),
        'token': new_token
    }})
    return {'token': new_token}


def db_update_info(token: str, **data) -> dict:
    """
    Обновление данных пользователем
    :param token: Токен
    :param data: Значения
    :return: Измененные поля
    """
    allowed_fields = {'first_name', 'second_name', 'about', 'gender', 'email'}
    fields = dict()
    for key in data:
        value = data[key]
        if key in allowed_fields:
            fields[key] = value

    result = db.get_collection('users').find_one_and_update({'token': token}, {'$set': fields}, {'_id': 1})
    if result is None:
        raise UpdateInfoError(50, "Введен неверный токен")
    return fields


class BaseResponseError(Exception):
    def __init__(self, error_id: int, message: str):
        self.error_id = error_id
        self.message = message


class RegistrationError(BaseResponseError):
    pass


class LoginError(BaseResponseError):
    pass


class ResetPasswordError(BaseResponseError):
    pass


class UpdateInfoError(BaseResponseError):
    pass
