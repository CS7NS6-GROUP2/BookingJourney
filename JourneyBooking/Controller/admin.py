import json
from flask import Blueprint
from flask import request, flash, redirect, url_for, render_template, Blueprint, session
from dao import *

admin = Blueprint("admin", __name__, template_folder='templates')


@admin.route('/management', methods=['GET', 'POST'])
def management():
    return render_template('admin_home.html')


@admin.route('/management/journey', methods=['GET', 'POST'])
def journey():
    all_journeys = get_all_journeys()
    if all_journeys is None:
        return render_template('Journey_manage.html', journeys="")
    return render_template('Journey_manage.html', journeys= json.loads(all_journeys))


@admin.route('/admin_approve')
def approve():
    return 'aaa'


@admin.route('/management/add')
def add():
    return render_template('add.html')
#
#
# @admin.route('/create_journey')
# def admin_create_journey():
#     name = ""
#     create_journey(name)
#     return "{}"