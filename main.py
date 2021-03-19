import flask

from json.encoder import JSONEncoder
from modules import methods, account_methods


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
    return flask.render_template("pages/index.html")


@app.route("/game/connect", methods=["POST", "GET"])
@account_methods.authorize_require
def game_connect_page():
    return flask.render_template("pages/game/connect.html")


@app.route("/game/create", methods=["POST", "GET"])
@account_methods.authorize_require
def game_create_page():
    return flask.render_template("pages/game/create.html")


@app.route("/game/editor", methods=["POST", "GET"])
@account_methods.authorize_require
def game_editor_page():
    return flask.render_template("pages/game/editor.html")


@app.route("/game/top")
def name_top_page():
    return flask.render_template("pages/game/table.html")


@app.route("/help/guide")
def info_guide_page():
    return flask.render_template("pages/info/guide.html")


@app.route("/profile", methods=["POST", "GET"])
@account_methods.authorize_require
def profile_page():
    return flask.render_template("pages/profile/index.html")


@app.route("/login", methods=["POST", "GET"])
@account_methods.not_authorize_require
def login_page():
    data = methods.login(**flask.request.form)
    if data['type'] == 'success':
        response = flask.make_response(flask.redirect("/profile"))
        response.set_cookie("auth", value=data['object']['token'], max_age=60*60*24*7)
        print(data['object']['token'])
        return response
    return flask.render_template("pages/profile/login.html")


@app.route("/register", methods=["POST", "GET"])
@account_methods.not_authorize_require
def register_page():
    data = methods.register(**flask.request.form)
    if data['type'] == 'success':
        response = flask.make_response(flask.redirect("/profile", 302))
        response.set_cookie("auth", value=data['object']['token'], max_age=60*60*24*7)
        return response
    return flask.render_template("pages/profile/register.html")


if __name__ == '__main__':
    app.run()
