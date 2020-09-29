from flask import Blueprint
from flask import render_template

bp = Blueprint('tea', __name__, url_prefix='/tea')

@bp.route('/<id>')
def display(id):
    return render_template('items/details.html')

@bp.route('/sell')
def sell():
    return render_template('items/listItem.html')

