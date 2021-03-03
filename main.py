import re
import flask

from json.encoder import JSONEncoder
from modules import methods


json_encoder = JSONEncoder()
app = flask.Flask(__name__)


@app.route("/api/register", methods=['POST'])
def register_api():
    response = flask.request.form
    return json_encoder.encode(methods.register(**response))


@app.route("/api/login", methods=['POST'])
def login_api():
    response = flask.request.form
    return json_encoder.encode(methods.login(**response))


if __name__ == '__main__':
    app.run()
