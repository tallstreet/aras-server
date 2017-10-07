from flask import Flask, request, g
import sqlite3
from flask_json import FlaskJSON, JsonError, json_response, as_json
from datetime import datetime
import json

app = Flask(__name__)
jsonapp = FlaskJSON(app)

DATABASE = 'database.db'


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


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


@app.route('/get_time')
def get_time():
    now = datetime.utcnow()
    return json_response(time=now)


@app.route("/")
def hello():
    return "ARAS"


@app.route('/config', methods=['PUT'])
@as_json
def config_set():
    new_config = request.get_json()
    cur = get_db().cursor()
    query = "update config set config = ?"
    cur.execute(query, [json.dumps(new_config)])
    get_db().commit()
    cur.close()
    return new_config


@app.route('/config', methods=['GET'])
@as_json
def config_get():
    query = "select config from config"
    cur = get_db().execute(query, [])
    rv = cur.fetchall()
    cur.close()
    config = rv[0][0] if rv else None
    return json.loads(config)


@app.route('/logs', methods=['GET'])
@as_json
def logs_get():
    query = "select * from logs"
    cur = get_db().execute(query, [])
    logs = cur.fetchall()
    cur.close()
    return logs
