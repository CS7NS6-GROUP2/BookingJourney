import json

from cassandra import ConsistencyLevel
from cassandra.query import BatchStatement, SimpleStatement
from cassandra_flask_sessions import AbstractConnectionProvider, CassandraSessionInterface
from flask import Flask, jsonify, session
from flask_login import LoginManager
from cassandra.cluster import Cluster

from Controller.admin import *
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


@login_manager.user_loader
def load_user(userid):
    print(userid)
    user = User.get(userid)
    return user


# Register Blueprints
app.register_blueprint(login)
app.register_blueprint(book)
app.register_blueprint(admin)

if __name__ == '__main__':
    app.run()
