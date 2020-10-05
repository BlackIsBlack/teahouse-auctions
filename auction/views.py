from flask import Blueprint
from flask import render_template
from .models import auctionListing
from flask_login import login_required, current_user
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    auctionItems = auctionListing.query.all()
    return render_template('index.html', items = auctionItems)

@bp.route('/watchlist')
@login_required
def watchlist():
    return render_template('watchlist.html')

