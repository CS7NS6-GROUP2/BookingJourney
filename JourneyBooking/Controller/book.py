import json

from flask import Blueprint
from flask import request, flash, redirect, url_for, render_template, Blueprint, session
from flask_login import current_user
from dao import *
book = Blueprint("book", __name__, template_folder='templates')


@book.route('/my_journeys')
def my_journeys():
    js = get_orders_by_user(current_user.id)
    print(js is None)
    if js is None:
        return render_template('myjourneys.html', orders = "")

    python_object = json.loads(js)
    counts = dict()
    l = list()
    for i, item in enumerate(python_object):
        if item["status"] == 0:
            item["status"] = "pending"
        else:
            item["status"] = "approved"
        if item["batchid"] in counts:
            index = counts[item["batchid"]]
            l[index]["orderid"] = l[index]["orderid"] + "</br>"
            l[index]["orderid"] =  l[index]["orderid"] + item["orderid"]
            l[index]["journeyid"] =  l[index]["journeyid"] + "</br>"
            l[index]["journeyid"] =  l[index]["journeyid"] + item["journeyid"]
        else:
            counts[item["batchid"]] = len(l)
            l.append(item)

    return render_template('myjourneys.html', orders=json.loads(json.dumps(python_object, indent=2)))


@book.route('/book_journey',methods=['POST'], strict_slashes=False)
def book_journey():
    data = request.data.decode('UTF-8')
    journeys = json.loads(data)["journeyList"]
    ids = []
    for list in journeys:
        ids.append(list[0])
    book_tickets(current_user.id, ids)
    return "{}"

@book.route('/cancel_journey',methods=['POST'], strict_slashes=False)
def cancel_booking():
    uid = current_user.id
    data = request.data.decode('UTF-8')
    journeys = json.loads(data)["journeyList"]
    ids = []


    for list in journeys:
        x = list[0].split("<br>")
        for id in x:
            ids.append(id)

    cancel_orders(uid, ids)
    return "{}"