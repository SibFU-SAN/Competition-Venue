import re
import modules.database as database


def r_error(code: int, description: str, **kwargs):
    """
    Генерация ответа ошибки
    :param code: Код ошибки
    :param description: Описание ошибки
    :param kwargs: Введенные поля метода
    :return: Ответ
    """
    response = {
        'type': 'error',
        'code': code,
        'description': description,
        'params': kwargs,
        'object': None
    }
    return response


def r_success(**kwargs):
    """
    Генерация ответа успешного запроса
    :param kwargs: Ключи для ответа в object
    :return: Ответ
    """
    response = {
        'type': 'success',
        'object': kwargs
    }
    return response


def register(**data) -> dict:
    """
    Регистрация пользователя и получение его токена.
    :param data: Параметры. Обязательные: login(String), password(String), confirmation(String)
    :return: Ошибка или результат в виде:
    {'object': {
        'token': String, // Токен пользователя
    }}
    """
    if not ('login' in data and
            'password' in data and
            'confirmation' in data):
        return r_error(20, 'Не заполнены все поля',
                       login=('login' in data),
                       password=('password' in data),
                       confirmation=('confirmation' in data))

    if data['password'] != data["confirmation"]:
        return r_error(21, 'Пароли не совпадают')

    if not(5 < len(data['password']) < 33):
        return r_error(24, 'Введена недопустимая длина пароля. Допустимый диапазон начинается от 6 до 32 символов')

    if not(3 < len(data['login']) < 33):
        return r_error(23, 'Введена недопустимая длина логина. Допустимый диапазон начинается от 4 до 32 символов')

    if not re.match("^[aA-zZ\\d]+$", data['login']):
        return r_error(22, 'В логине присутствуют недопустимые символы')

    try:
        token = database.db_create_user(data['login'], data['password'])
        return r_success(token=token)
    except database.RegistrationError as ex:
        return r_error(ex.error_id, ex.message)


def login(**data) -> dict:
    """
    Авторизация пользователя и получение его токена.
    :param data: Параметры. Обязательные: login(String), password(String)
    :return: Ошибка или результат в виде:
    {'object': {
        'token': String, // Токен пользователя
    }}
    """
    if not ('login' in data and
            'password' in data):
        return r_error(30, 'Не заполнены все поля',
                       login=('login' in data),
                       password=('password' in data))

    try:
        token = database.db_auth(data['login'], data['password'])
        return r_success(token=token)
    except database.LoginError as ex:
        return r_error(ex.error_id, ex.message)


def get_data(**data) -> dict:
    """
    Получение данных пользователя.
    :param data: Параметры. Обязательные: token(String)
    :return: Ошибка или результат в виде:
    {'object': {
        // Данные пользователя. Ключей может быть произволькое кол-во
    }}
    """
    if 'token' not in data:
        return r_error(30, "Не заполнены все поля",
                       token=('token' in data))

    try:
        result = database.db_get_user_data(data['token'], 'by_token' not in data or data['by_token'])
        return r_success(**result)
    except database.LoginError as ex:
        return r_error(ex.error_id, ex.message)


def reset_password(**data) -> dict:
    """
    Смена пароля пользователя и получение нового токена.
    :param data: Параметры. Обязательные: token(String), new_password(String)
    :return: Ошибка или результат в виде:
    {'object': {
       'token': String, // Новый токен пользователя
    }}
    """
    if not('token' in data and 'new_password' in data):
        return r_error(30, "Не заполнены все поля",
                       token=('token' in data),
                       new_password=('new_password' in data))

    if not(5 < len(data['password']) < 33):
        return r_error(41, 'Введена недопустимая длина пароля. Допустимый диапазон начинается от 6 до 32 символов')

    try:
        result = database.db_reset_password(data['token'], data['new_password'])
        return r_success(**result)
    except database.ResetPasswordError as ex:
        return r_error(ex.error_id, ex.message)


def update_data(**data) -> dict:
    """
    :param data: Параметры. Обязательные: token(String)
    :return: Ошибка или результат в виде:
    {'object': {
        // Данные пользователя. Ключей может быть произволькое кол-во
    }}
    """
    if 'token' not in data:
        return r_error(30, "Не заполнены все поля",
                       token=('token' in data))

    if 'gender' in data:
        data['gender'] = int(data['gender'])

    try:
        result = database.db_update_info(**dict(data))
        return r_success(**result)
    except database.UpdateInfoError as ex:
        return r_error(ex.error_id, ex.message)
