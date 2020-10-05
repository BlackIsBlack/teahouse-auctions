from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('tea', __name__, url_prefix='/tea')

@bp.route('/<id>')
def display(id):
    return render_template('items/details.html')

@bp.route('/sell')
@login_required
def sell():
    return render_template('items/listItem.html')

