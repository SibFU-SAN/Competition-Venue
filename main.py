import sys
import logging

import flask
import yaml

from json.encoder import JSONEncoder
from modules import methods, account_methods, database
from modules.game_handler import GameHandler

json_encoder = JSONEncoder()
app = flask.Flask(__name__,
                  static_folder="./templates/",
                  template_folder="./templates/"
                  )


@app.route("/api/register", methods=['POST'])
def register_api():
    return json_encoder.encode(methods.register(**flask.request.form))


@app.route("/api/login", methods=['POST'])
def login_api():
    return json_encoder.encode(methods.login(**flask.request.form))


@app.route("/api/user_data")
def user_data_api():
    return json_encoder.encode(methods.get_data(**flask.request.form))


@app.route("/api/user_data_update")
def user_data_update_api():
    return json_encoder.encode(methods.update_data(**flask.request.form))


@app.route("/")
def index_page():
    return flask.render_template("pages/index.html", auth=account_methods.is_authorized())


@app.route("/game/connect", methods=["POST", "GET"])
@account_methods.authorize_require
def game_connect_page():
    return flask.render_template("pages/game/connect.html", auth=True)


@app.route("/game/create", methods=["POST", "GET"])
@account_methods.authorize_require
def game_create_page():
    return flask.render_template("pages/game/create.html", auth=True)


@app.route("/game/editor", methods=["POST", "GET"])
@account_methods.authorize_require
def game_editor_page():
    return flask.render_template("pages/game/editor.html", auth=True)


@app.route("/game/top")
def name_top_page():
    return flask.render_template("pages/game/table.html", auth=account_methods.is_authorized())


@app.route("/help/guide")
def info_guide_page():
    return flask.render_template("pages/info/guide.html", auth=account_methods.is_authorized())


@app.route("/profile", methods=["POST", "GET"])
@account_methods.authorize_require
def profile_page():
    data = methods.get_data(token=account_methods.get_token())['object']
    return flask.render_template("pages/profile/index.html", auth=True, data=data, genders=genders)


@app.route("/target/<login>", methods=["POST", "GET"])
def other_profile_page(login):
    target_data = methods.get_data(token=account_methods.get_login_hash(login), by_token=False)['object']
    if target_data is not None:
        return flask.render_template("pages/profile/index.html",
                                     auth=account_methods.is_authorized(),
                                     data=target_data,
                                     genders=genders)
    # TODO: Сделать страницу-заглушку
    return flask.redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.route("/login", methods=["POST", "GET"])
@account_methods.not_authorize_require
def login_page():
    response = flask.request.form

    if len(response) == 0:
        return flask.render_template("pages/profile/login.html")

    data = methods.login(**response)
    if data['type'] == 'success':
        response = flask.make_response(flask.redirect("/profile"))
        response.set_cookie("auth", value=data['object']['token'], max_age=60 * 60 * 24 * 7)
        return response

    return flask.render_template("pages/profile/login.html", error=data['description'],
                                 passed_login=response['login'])


@app.route("/register", methods=["POST", "GET"])
@account_methods.not_authorize_require
def register_page():
    response = flask.request.form

    if len(response) == 0:
        return flask.render_template("pages/profile/register.html")

    data = methods.register(**response)
    if data['type'] == 'success':
        response = flask.make_response(flask.redirect("/profile", 302))
        response.set_cookie("auth", value=data['object']['token'], max_age=60 * 60 * 24 * 7)
        return response
    return flask.render_template("pages/profile/register.html", error=data['description'])


@app.route("/profile/sign_out")
def sign_out_page():
    response = flask.make_response(flask.redirect("/", 302))
    response.set_cookie("auth", "", 0)
    return response


@app.route("/profile/settings", methods=["POST", "GET"])
@account_methods.authorize_require
def settings_data():
    global genders
    response = flask.request.form
    token = account_methods.get_token()
    if len(response) != 0:
        methods.update_data(token=token, **response)
    data = methods.get_data(token=token)

    return flask.render_template("pages/profile/settings.html", auth=True, data=data['object'], genders=genders)


if __name__ == '__main__':
    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)
    logger_handler = logging.FileHandler('log.txt')
    logger_handler.setLevel(logging.INFO)
    logger_formatter = logging.Formatter('%(asctime)s | [%(levelname)s][%(name)s] %(message)s')
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    sys.excepthook = lambda ex_type, ex_value, tb: \
        logger.error("Logging an uncaught exception",
                     exc_info=(ex_type, ex_value, tb))
    logger.info("Запуск программы")

    db_options = {}
    try:
        with open("database.yml", 'r') as file:
            db_options = yaml.load(file.read(), Loader=yaml.FullLoader)
    except FileNotFoundError:
        logger.warning("Не найден файл с данными для подключения к базе данных. Создаю новый")

    with open("database.yml", 'w') as file:
        if 'host' not in db_options:
            db_options['host'] = "localhost"
        if 'port' not in db_options:
            db_options['port'] = "27017"
        if 'base' not in db_options:
            db_options['base'] = "test"
        if 'auth' not in db_options:
            db_options['auth'] = False
        if 'user' not in db_options:
            db_options['user'] = "userName"
        if 'password' not in db_options:
            db_options['password'] = "1234567890"
        if 'auth_base' not in db_options:
            db_options['auth_base'] = "admin"
        file.write(yaml.dump(db_options))
    database.connect(**db_options)

    genders = ('Мужской', 'Женский')

    handler = GameHandler(logger.getChild("GameHandler"))
    handler.start()

    app.run()
