from flask import Blueprint
from flask import render_template
from . import db
from .models import auctionListing

bp = Blueprint('details', __name__)

@bp.route('/<id>')
def details(id):
    details = auctionListing.query.filter_by(id=id).first()
    return render_template('/details.html', auctionListing=details)