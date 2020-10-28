from flask import Blueprint, render_template, request
from sqlalchemy import desc
from .models import auctionListing
from flask_login import login_required, current_user
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    auctionItems = auctionListing.query.filter_by(bid_status = 1).order_by(desc(auctionListing.start_time))
    hotItem = auctionItems.filter_by(bid_status = 1).order_by(desc(auctionListing.total_bids)).first()
    recentlySold = auctionListing.query.filter(auctionListing.current_bid != 0).filter_by(bid_status = 0).order_by(desc(auctionListing.end_time)).first()
    
    return render_template('index.html', items = auctionItems, hotItem = hotItem, recentlySold = recentlySold)

@bp.route('/watchlist')
@login_required
def watchlist():
    watchlistItems = Watchlist.query.filter_by(user_id=current_user.id)

    return render_template('watchlist.html', items=watchlistItems)

@bp.route('/profile')
@login_required
def profile():
    activeUserListings = auctionListing.query.filter_by(user_id = current_user.id, bid_status=1)
    completedUserListings = auctionListing.query.filter_by(user_id = current_user.id, bid_status=0)
    return render_template('profile.html', myActiveListings=activeUserListings, myCompletedListings = completedUserListings)
