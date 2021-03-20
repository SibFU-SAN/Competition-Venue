import flask
import modules.database as db


def is_authorized():
    token = flask.request.cookies.get("auth")
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
