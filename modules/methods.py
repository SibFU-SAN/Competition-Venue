import re
import modules.database as database


def r_error(code: int, description: str, **kwargs):
    response = {
        'type': 'error',
        'code': code,
        'description': description,
        'object': kwargs
    }
    return response


def r_success(**kwargs):
    response = {
        'type': 'success',
        'object': kwargs
    }
    return response


def register(**data) -> dict:
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
    if 'token' not in data:
        return r_error(30, "Не заполнены все поля",
                       token=('token' in data))

    try:
        result = database.db_get_user_data(data['token'])
        return r_success(**result)
    except database.LoginError as ex:
        return r_error(ex.error_id, ex.message)


def reset_password(**data) -> dict:
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
