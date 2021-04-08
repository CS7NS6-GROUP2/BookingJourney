from flask import request, flash, redirect, url_for, render_template, Blueprint
from flask_login import login_user, login_required, logout_user

from model.journey import JOURNEY
from model.user import User

login = Blueprint("login", __name__, template_folder='templates')


@login.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.get_user(username)
        if user is not None and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('login.index', name=user.username, journeys=JOURNEY))

        flash('Invalid username or password.')
        return redirect(url_for('login.log_in'))

    return render_template('login.html')


@login.route('/logout')
@login_required
def log_out():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@login.route('/index/<name>&<journeys>', methods=['GET', 'POST'])
# todo journeys list
def index(name, journeys):
    return render_template('index.html', name=name, journeys=JOURNEY)
