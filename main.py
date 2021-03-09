import flask

from json.encoder import JSONEncoder
from modules import methods


json_encoder = JSONEncoder()
app = flask.Flask(__name__)


@app.route("/api/register", methods=['POST'])
def register_api():
    return json_encoder.encode(methods.register(**flask.request.form))


@app.route("/api/login", methods=['POST'])
def login_api():
    return json_encoder.encode(methods.login(**flask.request.form))


if __name__ == '__main__':
    app.run()
