from flask import Flask
from flask_login import LoginManager

from Controller.login import *
from Controller.book import *
from model.user import User

app = Flask(__name__)
app.secret_key = 'abc'
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login.log_in'


@login_manager.user_loader
def load_user(userid):
    user = User.get(userid)
    return user


# Register Blueprints
app.register_blueprint(login)
app.register_blueprint(book)

if __name__ == '__main__':
    app.run()
