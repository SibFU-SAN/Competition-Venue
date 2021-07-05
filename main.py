import datetime
import sys
import os
import re
import logging

import flask
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import yaml

import app.form as forms
from json.encoder import JSONEncoder
import snake.handler as sh
from app.database import db
import app.user as u
from app.user.constants import LOGIN_REGEX


json_encoder = JSONEncoder()
app = flask.Flask(__name__,
                  static_folder="./templates/",
                  template_folder="./templates/"
                  )
app.config['SECRET_KEY'] = 'ITS IS NOT SECRET KEY'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"

# Логгер
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
logger_handler = logging.FileHandler('log.txt', encoding='utf-8')
logger_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s | [%(levelname)s][%(name)s] %(message)s')
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)
sys.excepthook = lambda ex_type, ex_value, tb: \
    logger.error("Logging an uncaught exception",
                 exc_info=(ex_type, ex_value, tb))
logger.info("Запуск программы")

# Подключение к базе данных
db_options = {}
try:
    with open("database.yml", 'r') as file:
        db_options = yaml.load(file.read(), Loader=yaml.FullLoader)
except FileNotFoundError:
    logger.warning("Не найден файл с данными для подключения к базе данных. Создаю новый")
with open("database.yml", 'w') as file:
    if 'host' not in db_options:
        db_options['host'] = "localhost"
    if 'base' not in db_options:
        db_options['base'] = "test"
    if 'user' not in db_options:
        db_options['user'] = "root"
    if 'password' not in db_options:
        db_options['password'] = "1234567890"
    file.write(yaml.dump(db_options))

app.config['MYSQL_DATABASE_USER'] = db_options['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db_options['password']
app.config['MYSQL_DATABASE_DB'] = db_options['base']
app.config['MYSQL_DATABASE_HOST'] = db_options['host']
db.init_app(app)

# Создание папок с контентом
for path in (
            "./resources",
            "./resources/scripts",
            "./resources/demos"
            ):
    if not os.path.exists(path):
        os.mkdir(path)

# Старт обработчика игр
handler = sh.GameHandler(logger.getChild("GameHandler"))
handler.start()

logger.info("Запуск веб-сервера")


@login_manager.user_loader
def load_user(uid) -> u.User or None:
    return u.get_by_id(int(uid))


@app.route("/404")
@app.errorhandler(404)
def err404(_=None):
    return flask.render_template("pages/404.html", user=current_user)


@app.errorhandler(500)
def err500(_):
    return flask.render_template("pages/500.html", user=current_user), 500


@app.route("/login", methods=["post", "get"])
def login_page():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("profile"))

    form = forms.LoginForm()
    error = None
    if form.is_submitted():
        login = form.login.data
        password = form.password.data

        user = u.auth(login, password)

        if user is not None:
            login_user(user, True, datetime.timedelta(weeks=2))
            return flask.redirect("profile")
        else:
            error = "Неверный логин и пароль"

    return flask.render_template("pages/profile/login.html", form=form, error=error)


@app.route("/register", methods=["post", "get"])
def register_page():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("profile"))

    form = forms.RegisterForm()
    error = None
    if form.is_submitted():
        login = form.login.data.strip()
        password = form.password.data
        confirmation = form.confirmation.data

        if not re.match(LOGIN_REGEX, login):
            error = "Логин может быть только состоять из английских букв и нижнего подчеркивания"
        if len(password) < 5:
            error = "Пароль слишком короткий"
        if password != confirmation:
            error = "Пароли не совпадают"

        try:
            u.register(login, password)
        except u.UserError as ex:
            error = ex.message

        if error is None:
            return flask.redirect(flask.url_for("login_page"))

    return flask.render_template("pages/profile/register.html", form=form, error=error)


@app.route("/logout")
def logout_page():
    logout_user()
    return flask.redirect(flask.url_for("index_page"))


@app.route("/")
@app.route("/index")
def index_page():
    return flask.render_template("pages/index.html", user=current_user)


@app.route("/profile")
@login_required
def profile_page():
    return flask.render_template("pages/profile/index.html", user=current_user, target=current_user)


@app.route("/target/<login>")
def other_profile_page(login):
    target = u.get_by_login(login)
    if target is None:
        return err404()
    return flask.render_template("pages/profile/index.html", user=current_user, target=target)


@app.route("/top")
def top_page():
    top = u.get_top10()
    return flask.render_template("pages/top.html", user=current_user, top=top)


if __name__ == '__main__':
    app.run()
