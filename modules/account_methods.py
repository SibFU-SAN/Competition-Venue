import hashlib
import flask
import modules.database as db
import os


def is_authorized():
    token = get_token()
    if token is None:
        return False
    return db.db_check_token(token)


def authorize_require(func):
    def check_auth():
        if is_authorized():
            response = flask.make_response(func())
            response.set_cookie("auth", value=flask.request.cookies.get("auth"), max_age=60*60*24*7)
            return response
        return flask.redirect("/login", 302)

    check_auth.__name__ = func.__name__
    return check_auth


def not_authorize_require(func):
    def check_no_auth():
        if is_authorized():
            return flask.redirect("/profile")
        return func()

    check_no_auth.__name__ = func.__name__
    return check_no_auth


def get_token() -> str or None:
    return flask.request.cookies.get("auth")


def get_login_hash(login: str) -> str:
    return hashlib.md5(login.lower().encode()).hexdigest()


def save_script(game_id: str, user_id: str, script: str):
    if not os.path.exists(f"./resources/scripts/{game_id}"):
        os.mkdir(f"./resources/scripts/{game_id}")

    with open(f'./resources/scripts/{game_id}/{user_id}.py', 'w', encoding="utf-8") as file:
        file.write(script)


def read_script(game_id: str, user_id: str) -> str:
    if not os.path.exists(f"./resources/scripts/{game_id}"):
        return ""
    if not os.path.exists(f"./resources/scripts/{game_id}/{user_id}.py"):
        return ""

    with open(f'./resources/scripts/{game_id}/{user_id}.py', 'r', encoding="utf-8") as file:
        return file.read()


def load_demo(game_id: str) -> str or None:
    if not os.path.exists(f"./resources/demos/{game_id}"):
        return None
    with open(f'./resources/demos/{game_id}', 'r') as file:
        return file.read()
