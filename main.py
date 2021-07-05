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
import app.game as g
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


@app.route("/settings", methods=["post", "get"])
@login_required
def settings_page():
    settings = forms.SettingsForm()
    settings.about.data = current_user.about
    if settings.is_submitted():
        about = settings.about.data

        current_user.edit_settings(about)

    error = None
    password_form = forms.ChangePasswordForm()
    if password_form.is_submitted():
        password = u.hash_password(password_form.password.data)
        new_password = password_form.new_password.data
        confirmation = password_form.confirmation.data

        if password != current_user.hashed_password:
            error = "Введен неверный пароль"
        if new_password != confirmation:
            error = "Пароль не совпадают"
        if len(new_password) < 5:
            error = "Новый пароль слишком короткий"
        if error is None:
            current_user.change_password(new_password)

    return flask.render_template("pages/profile/settings.html",
                                 user=current_user, settings=settings, password_form=password_form, error=error)


@app.route("/watch/<int:game_id>")
def watch_page(game_id: int):
    game = g.get_by_id(game_id)
    if game is None:
        return err404()

    if game.status != g.constants.HANDLED:
        return flask.redirect(flask.url_for("game_page", game_id=game_id))

    if game.has_demo:
        return err404()

    return flask.render_template("pages/game/watch.html", user=current_user, game=game)


@app.route("/game/<int:game_id>")
@login_required
def game_page(game_id: int):
    game = g.get_by_id(game_id)
    if game is None:
        return err404()

    return flask.render_template("pages/game/info.html", user=current_user, game=game, constants=g.constants)


@app.route("/demos")
def demos_page():
    # TODO: Список демок
    return ""


@app.route("/editor")
@login_required
def editor_page():
    # TODO: Редактор кода
    return ""


@app.route("/connect")
@login_required
def connect_page():
    # TODO: Поиск комнат
    return ""


@app.route("/join/<int:game_id>")
@login_required
def join_page(game_id: int):
    # TODO: Вход в комнату
    return ""


@app.route("/create")
@login_required
def create_game_page():
    # TODO: Создание игры
    return ""


if __name__ == '__main__':
    app.run()
