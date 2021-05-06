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

@admin.route('/management/users', methods=['GET', 'POST'])
def users():
    all_users = get_all_users()
    if all_users is None:
        return render_template('user_manage.html', journeys="")
    return render_template('user_manage.html', users= json.loads(all_users))

@admin.route('/management/booking')
def approve():
    js = get_all_orders()
    if js is None:
        return render_template('booking_manage.html', orders = "")

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
            l[index]["orderid"] =  l[index]["orderid"] + item["orderid"]
            l[index]["journeyid"] =  l[index]["journeyid"] + "</br>"
            l[index]["journeyid"] =  l[index]["journeyid"] + item["journeyid"]
        else:
            counts[item["batchid"]] = len(l)
            l.append(item)

    return render_template('booking_manage.html', orders=json.loads(json.dumps(python_object, indent=2)))


@admin.route('/management/booking/approve',methods=['POST'], strict_slashes=False)
def approve_booking():
    data = request.data.decode('UTF-8')
    journeys = json.loads(data)["approvalList"]
    d = {}
    for list in journeys:
        uid = list[0]
        x = list[1].split("<br>")
        if uid not in d:
            d[uid] = []

        for orderId in x:
            d[uid].append(orderId)
    print(d)
    approve_orders(d)
    return "{}"
#
#
# @admin.route('/create_journey')
# def admin_create_journey():
#     name = ""
#     create_journey(name)
#     return "{}"
