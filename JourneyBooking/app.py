from flask import Flask
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


# cluster = Cluster([])

# @app.route('/')
# def hello_world():
#     cluster = Cluster([])
#     session = cluster.connect('test_22')
#     rows = session.execute("select JSON * from test_table")
#     for row in rows:
#         print(row)
#     return 'Hello World!'

@login_manager.user_loader
def load_user(userid):
    user = User.get(userid)
    return user


# Register Blueprints
app.register_blueprint(login)
app.register_blueprint(book)

if __name__ == '__main__':
    app.run()
