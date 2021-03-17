import flask

from json.encoder import JSONEncoder
from modules import methods


json_encoder = JSONEncoder()
app = flask.Flask(__name__,
                  static_folder="./templates/static/",
                  static_host="./templates/pages/"
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


if __name__ == '__main__':
    app.run()
