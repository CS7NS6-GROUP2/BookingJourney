from flask import Flask
from flask_login import LoginManager

from Controller.login import *
from Controller.book import *
from model.user import User

app = Flask(__name__)
app.secret_key = 'abc'
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    return user


# Register Blueprints
app.register_blueprint(login)
app.register_blueprint(book)

if __name__ == '__main__':
    app.run()
