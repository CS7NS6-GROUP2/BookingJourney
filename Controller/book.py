from flask import Blueprint

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
