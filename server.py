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
    return app.send_static_file('index.html')


@app.route('/config', methods=['PUT'])
@as_json
def config_set():
    new_config = request.get_json()
    cur = get_db().cursor()
    query = "update config set config = ?, overall = ?, p1_sms = ?, p2_sms = ?, p3_sms = ?, p1_voip = ?, p2_voip = ?, p3_voip = ?"
    cur.execute(query, [json.dumps(new_config), new_config['overall'], new_config['p1_sms'], new_config['p2_sms'],
                        new_config['p3_sms'], new_config['p1_voip'], new_config['p2_voip'], new_config['p3_voip']])
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
    query = "select *, rowid from logs"
    cur = get_db().execute(query, [])
    logs = cur.fetchall()
    cur.close()
    return logs


@app.route('/status', methods=['PATCH'])
@as_json
def state_update():
    status = request.get_json()
    cur = get_db().cursor()
    query = "update logs set status = ? where rowid = ?"
    cur.execute(query, [status["status"], status["rowid"]])
    get_db().commit()
    cur.close()
    return True


@app.route('/rangers', methods=['GET'])
@as_json
def rangers_get():
    query = "select *, rowid from rangers"
    cur = get_db().execute(query, [])
    logs = cur.fetchall()
    cur.close()
    return logs


@app.route('/ranger', methods=['PATCH'])
@as_json
def ranger_update():
    ranger = request.get_json()
    cur = get_db().cursor()
    query = "update rangers set name = ?, lat = ?, lon = ?, phone = ? where rowid = ?"
    cur.execute(query, [ranger["name"], ranger["lat"],
                        ranger["lon"], ranger["phone"], ranger["rowid"]])
    get_db().commit()
    cur.close()
    return True


@app.route('/ranger', methods=['POST'])
@as_json
def ranger_add():
    ranger = request.get_json()
    print(ranger)
    cur = get_db().cursor()
    query = "insert into rangers values (?, ?, ?, ?)"
    cur.execute(query, [ranger["name"], ranger["lat"],
                        ranger["lon"], ranger["phone"]])
    get_db().commit()
    cur.close()
    return True


@app.route('/ranger', methods=['DELETE'])
@as_json
def ranger_delete():
    ranger = request.get_json()
    cur = get_db().cursor()
    query = "delete from rangers where rowid = ?"
    cur.execute(query, [ranger["rowid"]])
    get_db().commit()
    cur.close()
    return True
