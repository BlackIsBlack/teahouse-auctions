from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import desc, asc
from .models import auctionListing, Watchlist, Bid
from flask_login import login_required, current_user
from .submitFields import getURLParams, getSortOrder, getWatchlistSortOrder
from datetime import datetime, timedelta
from . import db
bp = Blueprint('main', __name__)


@bp.route('/') 
def index():
    isSold = 1
    if(request.args.get('isSold')=='1'):
        isSold = 0
    # Gets a list of all auction items that are currently active
    allActives = auctionListing.query.filter_by(bid_status = isSold).order_by(desc(auctionListing.start_time))

    for currentItem in allActives:
        remainingTime = (currentItem.end_time - datetime.now()) # get time
        # close down auction
        if(remainingTime < timedelta(0)):
            currentItem.bid_status = 0
            db.session.commit()

    # If there are any URL parameters for filtering, run the getURLParams function to create a new filtering query.
    if(len(request.args)>0):
        auctionItems = eval(f"auctionListing.query.filter_by(bid_status = {isSold}){getURLParams(request)}.order_by({getSortOrder(request)})")
    # If not, use the normal query
    else:
        auctionItems = allActives
    # A hot item is selected by choosing the active item that has the most bids.
    hotItem = auctionListing.query.filter_by(bid_status = 1).order_by(desc(auctionListing.total_bids)).first()
    # Recently sold grabs the most recent auction with a non zero selling price
    recentlySold = auctionListing.query.filter(auctionListing.current_bid != 0).filter_by(bid_status = 0).order_by(desc(auctionListing.end_time)).first()
    
    if(isSold == 1):
        return render_template('index.html', items = auctionItems.order_by(desc(auctionListing.start_time)), hotItem = hotItem, recentlySold = recentlySold)
    else:
        return render_template('soldItems.html', items = auctionItems.order_by(desc(auctionListing.start_time)))

@bp.route('/sold')
def sold():
    return redirect(url_for('main.index',isSold = 1))


@bp.route('/watchlist')
@login_required
def watchlist():
    # The watchlist DB is queried for all items belonging to the logged in user.
    watchlistItems = Watchlist.query.filter_by(user_id=current_user.id)
    if(len(request.args)>0):
        watchlistItems = eval(f"Watchlist.query.filter_by(user_id=current_user.id).order_by({getWatchlistSortOrder(request)})")
    watchlistedAuctionItems = []
    # All the watchlist items are compared againsted the auctionListing db and added to a list to be displayed.
    for item in watchlistItems:
        watchlistedAuctionItems += auctionListing.query.filter_by(id=item.item_id)

    return render_template('watchlist.html', items=watchlistedAuctionItems)

@bp.route('/profile')
@login_required
def profile():
    # All of the user's listings (completed, and active) are queried using the bid status field.
    activeUserListings = auctionListing.query.filter_by(user_id = current_user.id, bid_status=1)
    completedUserListings = auctionListing.query.filter_by(user_id = current_user.id, bid_status=0)

    return render_template('profile.html', myActiveListings=activeUserListings, myCompletedListings = completedUserListings)


@bp.route('/bids')
@login_required
def bids():
    bids = Bid.query.filter_by(user_id = current_user.id)
    return render_template('profileBids.html', bids = bids)