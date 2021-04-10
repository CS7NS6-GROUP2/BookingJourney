from flask import request, flash, redirect, url_for, render_template, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

from model.journey import JOURNEY
from model.user import User

login = Blueprint("login", __name__, template_folder='templates')


@login.route('/')
def home():
    return render_template('home.html')


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
            login_user(user, True)
            return redirect(url_for('login.index'))

        flash('Invalid username or password.')
        return redirect(url_for('login.log_in'))

    return render_template('login.html')


@login.route('/logout')
@login_required
def log_out():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('login.log_in'))


@login.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            flash('Please confirm the password!')
        elif User.get_user(request.form['username']):
            flash('The username is already existed!')
        else:
            # add user
            # flash("Success！")
            return redirect(url_for('login.log_in'))

    return render_template('register.html')


@login.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', journeys=JOURNEY)
