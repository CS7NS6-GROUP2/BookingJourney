import json

from cassandra import ConsistencyLevel
from cassandra.query import BatchStatement, SimpleStatement
from cassandra_flask_sessions import AbstractConnectionProvider, CassandraSessionInterface
from flask import Flask, jsonify, session
from flask_login import LoginManager
from cassandra.cluster import Cluster
from Controller.login import *
from Controller.book import *
from model.user import User
from dao import connection


class ConnectionProvider(AbstractConnectionProvider):

    def __init__(self):
        self.__connection = connection

    def get_connection(self):
        return self.__connection


app = Flask(__name__)
app.secret_key = 'abc'
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login.log_in'
app.session_interface = CassandraSessionInterface(ConnectionProvider())


# cluster = Cluster(["35.172.217.174"])
# session = cluster.connect('group2')


@app.route('/set/<name>')
def set_session(name):
    session['name'] = name
    return 'ok'


@app.route('/get')
def get_session():
    return json.dumps(dict(session))


@app.route('/del')
def delete_session():
    session.clear()
    return 'ok'


@app.route('/admin_get_info')
def admin_get_info():
    admin_id = 20305559
    user_lookup_stmt = connection.prepare("SELECT JSON * FROM admin WHERE id=?")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = connection.execute(user_lookup_stmt, [admin_id])

    # {"id": 20305559, "name": "Rui", "password": "123456"}
    return results.one().json


@app.route('/user_register')
def user_register():
    name = "user1"
    car = "BMW 3"
    password = "123"
    id = uuid.uuid1()
    query = SimpleStatement(
        "INSERT INTO users (id, name, car, password) VALUES (%s, %s, %s, %s)",
        consistency_level=ConsistencyLevel.QUORUM)
    results = session.execute(query, (id, name, car, password))
    return "111"


@app.route('/user_auto_login')
def user_auto_login():
    sessionId = "4a79c304-a6a9-11eb-9b7c-acde48001122"
    user_lookup_stmt = session.prepare("SELECT * FROM session WHERE id={}".format(sessionId))
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt)
    print(results.one())
    if None == results.one():
        return "invaild"
    return "vaild"


@app.route('/user_login')
def user_login():
    id = " c85bc2dc-a455-11eb-aca6-acde48001122"
    password = "123"
    # login
    user_lookup_stmt = session.prepare("SELECT password FROM users WHERE id={}".format(id))
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt)

    # {"id": "51d1932a-a456-11eb-8231-acde48001122", "car": "BMW 3", "name": "user1", "password": "123"}
    pwd = results.one().password
    print(pwd)
    if pwd != password:
        return "password wrong"

    sessionId = uuid.uuid1()
    query = SimpleStatement(
        "INSERT INTO session (id) VALUES ({}) USING TTL 300 ".format(sessionId),
        consistency_level=ConsistencyLevel.QUORUM)
    results = session.execute(query)
    return str(sessionId)


@app.route('/create_journey')
def create_journey():
    id = uuid.uuid1()
    print(id)
    name = "journey1"
    available = 10

    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    batch.add(SimpleStatement("INSERT INTO journey_info (id, name ) VALUES (%s, %s)"), (id, name))
    result = session.execute(batch)
    print(result.one())
    return "11"


@app.route('/get_all_journey')
def get_all_journeys():
    user_lookup_stmt = connection.prepare("SELECT JSON * FROM journey_info")
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = connection.execute(user_lookup_stmt)
    ans = "["
    for r in results:
        print(r.json)
        ans += r.json + ","
    ans = ans[:-1]
    ans += ']'
    print(ans)
    return ans


@app.route('/book_one_ticket')
def book_one_ticket():
    uid = "e04c6afa-a558-11eb-8449-acde48001122"
    orderid = uuid.uuid1()
    journeys = "e04c6afa-a558-11eb-8449-acde48001122"
    batchId = uuid.uuid1()
    user_lookup_stmt = session.prepare(
        "insert into orders (orderid, userid, journeyId, batchId, status) VALUES ({}, {}, {}, {}, {}) ".format(
            orderid, uid, journeys, batchId, 0
        ))
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt)
    return "--"








@app.route('/cancel_one_order')
def cancel_one_order():
    orderid = "592d9ff6-a6ae-11eb-a85f-acde48001122"
    uid = "e04c6afa-a558-11eb-8449-acde48001122"
    user_lookup_stmt = session.prepare("update orders set status = -1 "
                                       "where orderid = {} and userid = {} ;".format(orderid, uid))
    user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
    results = session.execute(user_lookup_stmt)
    return "--"


@login_manager.user_loader
def load_user(userid):
    print(userid)
    user = User.get(userid)
    return user


# Register Blueprints
app.register_blueprint(login)
app.register_blueprint(book)

if __name__ == '__main__':
    app.run()
