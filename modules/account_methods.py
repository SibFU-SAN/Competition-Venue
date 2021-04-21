import hashlib
import flask
import modules.database as db


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
