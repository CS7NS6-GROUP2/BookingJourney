import uuid

from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement, BatchStatement, BatchType
from flask import Flask, json, jsonify
from flask_login import LoginManager
from cassandra.cluster import Cluster
from Controller.login import *
from Controller.book import *
from model.user import User

app = Flask(__name__)
app.secret_key = 'abc'
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login.log_in'


cluster = Cluster(["18.205.60.230", "54.210.238.122", "34.239.180.190"])
session = cluster.connect('group2')

@app.route('/admin_get_info')
def admin_get_info():


    admin_id = 20305559
    user_lookup_stmt = session.prepare("SELECT JSON * FROM admin_table WHERE id=?")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt, [admin_id])

    # {"id": 20305559, "name": "Rui", "password": "123456"}
    return results.one().json



# CREATE TABLE admin
# id int PRIMARY KEY ,
# name text,
# password text,
# ) WITH caching = { 'keys' : 'ALL', 'rows_per_partition' : '20' };
#
#
#
# CREATE TABLE users(
# id uuid PRIMARY KEY ,
# name text,
# car text,
# password text,
# ) WITH caching = { 'keys' : 'ALL', 'rows_per_partition' : '100' };
#
# CREATE TABLE IF NOT EXISTS journey_info(
# id uuid PRIMARY KEY ,
# name text,
# ) WITH caching = { 'keys' : 'ALL', 'rows_per_partition' : '120' };
#
#
#
#
# CREATE TABLE IF NOT EXISTS journey_ticket (
# id uuid,
# name text,
# available int,
# PRIMARY KEY (id, name)
# ) WITH caching = { 'keys' : 'ALL', 'rows_per_partition' : '120' };

@app.route('/login')
def user_login():
    id = uuid.uuid1()
    name = "user1"
    car = "BMW 3"
    password = "123"

    query = SimpleStatement(
        "INSERT INTO users (id, name, car, password) VALUES (%s, %s, %s, %s)",
        consistency_level=ConsistencyLevel.QUORUM)
    results = session.execute(query,  (id, name, car, password))

    # login
    user_lookup_stmt = session.prepare("SELECT JSON * FROM users WHERE id=?")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt, [id])

    # {"id": "51d1932a-a456-11eb-8231-acde48001122", "car": "BMW 3", "name": "user1", "password": "123"}
    return results.one().json

@app.route('/create_journey')
def create_journey():
    id = uuid.uuid1()
    print(id)
    name = "journey1"
    available = 10

    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    batch.add(SimpleStatement("INSERT INTO journey_info (id, name ) VALUES (%s, %s)"), (id, name))
    batch.add(SimpleStatement("INSERT INTO journey_ticket (id, name, available ) "
                              "VALUES (%s, %s, %s)"), (id, name, available))
    result = session.execute(batch)
    print(result.one())
    return "11"


@app.route('/get_all_journey')
def get_all_journeys():
    user_lookup_stmt = session.prepare("SELECT JSON * FROM journey_info")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt)
    return jsonify(results.all())



@app.route('/book_one_ticket')
def book_one_ticket():
    journeys_id = "e04c6afa-a558-11eb-8449-acde48001122"
    user_lookup_stmt = session.prepare("SELECT available FROM journey_ticket where id = {}".format(journeys_id))
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt)
    available = results.one()[0]
    print(available)
    if available <= 0:
        return
    uid = "e04c6afa-a558-11eb-8449-acde48001122"
    order_id = uuid.uuid1()
    batch_id = uuid.uuid1()
    name = " journey1"

    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    batch.add(SimpleStatement("UPDATE journey_ticket "
                              "SET available={}  "
                              "WHERE id={} AND name='{}'"
                              .format(available - 1, journeys_id, name)))

    batch.add(SimpleStatement("INSERT INTO ticket_order (id, uid, jid, batch_id, status) VALUES ({}, {}, {}, {},{})".
                              format(order_id, uid, journeys_id, batch_id, 0)))
    r = session.execute(batch)
    return "--"


@app.route('/query_available')
def query_available():
    journey_id = "ad9e75c-a491-11eb-8f23-acde48001122"

    user_lookup_stmt = session.prepare("SELECT available FROM journey_ticket where id = ".format(journey_id))
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM

    results = session.execute(user_lookup_stmt)
    return results.all().json

@app.route('/query_available')
def get_orders():
    # TODO
    u_id = "42658ed0-a566-11eb-ab38-acde48001122"
    user_lookup_stmt = session.prepare("SELECT JSON * FROM journey_ticket where uid = {} and status >= 0".format(u_id))
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt)
    return results.all().json





@login_manager.user_loader
def load_user(userid):
    user = User.get(userid)
    return user


# Register Blueprints
app.register_blueprint(login)
app.register_blueprint(book)

if __name__ == '__main__':
    app.run()
