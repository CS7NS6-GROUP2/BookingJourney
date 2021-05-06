import json
from flask import Blueprint
from flask import request, flash, redirect, url_for, render_template, Blueprint, session

admin = Blueprint("admin", __name__, template_folder='templates')


@admin.route('/management', methods=['GET', 'POST'])
def management():
    return render_template('admin_home.html')


@admin.route('/admin_approve')
def approve():
    return 'aaa'
#
#
# @admin.route('/create_journey')
# def admin_create_journey():
#     name = ""
#     create_journey(name)
#     return "{}"