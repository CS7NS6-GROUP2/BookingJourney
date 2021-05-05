from flask import Blueprint
from flask import request, flash, redirect, url_for, render_template, Blueprint, session

book = Blueprint("book", __name__, template_folder='templates')


@book.route('/prebook/<driver_id>')
def prebook_journey(driver_id):
    return 'aaa'


@book.route('/prebook/<int:order_id>')
def cancel_journey(order_id):
    return 'aaa'


@book.route('/order/<driver_id>')
def get_order(driver_id):
    return 'aaa'


@book.route('/book_journey',methods=['POST'], strict_slashes=False)
def book_journey():
    print("list from submit")
    print(request.data)
    return "{}"