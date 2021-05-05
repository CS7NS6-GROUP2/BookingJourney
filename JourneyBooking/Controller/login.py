import uuid
from flask import request, flash, redirect, url_for, render_template, Blueprint, session
from flask_login import login_user, login_required, logout_user, current_user
from model.journey import JOURNEY
from model.user import User
from cassandra import ConsistencyLevel
from cassandra.query import BatchStatement, SimpleStatement
from dao import connection

login = Blueprint("login", __name__, template_folder='templates')


@login.route('/')
def home():
    return render_template('home.html')


@login.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']

        if not userid or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.get(userid)

        if user is not None and user.validate_pwd(password):
            login_user(user, True)
            session['name'] = userid
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
        else:
            # add user
            name = request.form['username']
            car = request.form['car']
            password = request.form['password1']
            id = uuid.uuid1()
            query = SimpleStatement(
                "INSERT INTO users (id, name, car, password) VALUES (%s, %s, %s, %s)",
                consistency_level=ConsistencyLevel.QUORUM)
            results = connection.execute(query, (id, name, car, password))
            flash("You have registered successfully!Please remember your login ID: " + str(id))
            return redirect(url_for('login.log_in'))
    return render_template('register.html')


@login.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', journeys=JOURNEY)
