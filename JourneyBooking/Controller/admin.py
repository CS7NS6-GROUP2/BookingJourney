import json
from flask import Blueprint
from flask import request, flash, redirect, url_for, render_template, Blueprint, session
from dao import *
import re

admin = Blueprint("admin", __name__, template_folder='templates')


@admin.route('/management', methods=['GET', 'POST'])
def management():
    return render_template('admin_home.html')


@admin.route('/management/journey', methods=['GET', 'POST'])
def journey():
    all_journeys = get_all_journeys()
    if all_journeys is None:
        return render_template('Journey_manage.html', journeys="")
    return render_template('Journey_manage.html', journeys=json.loads(all_journeys))


@admin.route('/management/users', methods=['GET', 'POST'])
def users():
    all_users = get_all_users()
    if all_users is None:
        return render_template('user_manage.html', journeys="")
    return render_template('user_manage.html', users=json.loads(all_users))


@admin.route('/management/booking')
def booking():
    js = get_all_orders()
    if js is None:
        return render_template('booking_manage.html', orders="")

    python_object = json.loads(js)
    counts = dict()
    l = list()
    for i, item in enumerate(python_object):
        if item["status"] == 0:
            item["status"] = "pending"
        elif item["status"] == 1:
            item["status"] = "approved"
        else:
            item["status"] = "canceled"
        if item["batchid"] in counts:
            index = counts[item["batchid"]]
            l[index]["orderid"] = l[index]["orderid"] + "</br>"
            l[index]["orderid"] = l[index]["orderid"] + item["orderid"]
            l[index]["journeyid"] = l[index]["journeyid"] + "</br>"
            l[index]["journeyid"] = l[index]["journeyid"] + item["journeyid"]
        else:
            counts[item["batchid"]] = len(l)
            l.append(item)

    return render_template('booking_manage.html', orders=json.loads(json.dumps(l, indent=2)))


@admin.route('/management/add')
def add():
    return render_template('add.html')


@admin.route('/management/add_journey', methods=['POST'], strict_slashes=False)
def add_journey():
    name = request.form['new_journey']
    create_journey(name)
    return redirect(url_for('admin.journey'))


@admin.route('/management/approve', methods=['POST'], strict_slashes=False)
def approve():
    data = request.data.decode('UTF-8')
    print(data)
    l = re.split('=|&',data)
    orders = l[1].split('%3C%2Fbr%3E')
    uid = l[3]
    approve_orders(uid, orders)
    return {}

@admin.route('/management/reject', methods=['POST'], strict_slashes=False)
def reject():
    data = request.data.decode('UTF-8')
    print(data)
    l = re.split('=|&',data)
    orders = l[1].split('%3C%2Fbr%3E')
    uid = l[3]
    cancel_orders(uid, orders)
    return {}

@admin.route('/management/del_user', methods=['POST'], strict_slashes=False)
def del_user():
    return "del"
