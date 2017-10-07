from flask import Flask, request, g
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def hello():
    return "ARAS"


@app.route('/config', methods=['PUT'])
def config_set():
    print(request.get_json())
    setattr(g, 'config', request.get_json())
    return "set"


@app.route('/config', methods=['GET'])
def config_get():
    print(getattr(g, 'config', None))
    return "get"
