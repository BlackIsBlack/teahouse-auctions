from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from .forms import ItemForm, BidForm
from .models import auctionListing, User, Bid, Watchlist
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from . import db
bp = Blueprint('tea', __name__, url_prefix='/tea')

  # a new function
def check_upload_file(form):
  fp=form.photos.data
  filename=fp.filename
  BASE_PATH=os.path.dirname(__file__)

  upload_path=os.path.join(BASE_PATH,'static/image/itemImages/',secure_filename(filename))
  db_upload_path='/static/image/itemImages/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

# specific item page
@bp.route('/<id>', methods = ['GET','POST'])
def display(id):
    currentItem = auctionListing.query.filter_by(id=id).first() # get current item
    remainingTime = (currentItem.end_time - datetime.now()) # get time

    # close down auction
    if(remainingTime < timedelta(0)):
      currentItem.bid_status = 0
      db.session.commit()

    # fetch username
    userName = User.query.filter_by(id=currentItem.user_id).first().username

    # fetch bidlist if it's the owner
    bidList = []

    if (current_user.is_authenticated):

        if (current_user.id == currentItem.user_id):

            bidList = Bid.query.filter_by(listing_id = currentItem.id).order_by(desc(Bid.bid_time))
    
    # compile ingredient list
    ingredientList = currentItem.tea_name.split(',')

    form = BidForm()

    # placing a bid
    if (current_user.id == currentItem.user_id): # check user isn't the same as item's owner
  
      # form has been submitted
      if form.validate_on_submit():
          
          # bid must be higher than current bid
          if ((int)(form.bidAmount.data) > currentItem.current_bid):

              # setup query
              bidQuery = Bid(user_id = current_user.id, listing_id = currentItem.id, bid_amount = form.bidAmount.data, bid_time = datetime.now(), bid_status = 1)
              db.session.add(bidQuery)
              db.session.commit()

              # modify auctionlisting's current bid to equal bid amount 
              currentItem.current_bid = form.bidAmount.data
              db.session.query(auctionListing).filter(auctionListing.id == currentItem.id).update({"current_bid": currentItem.current_bid})
              db.session.commit()
          
          else:

              print("error") # gotta do something here

    return render_template('items/details.html', form=form, auctionListing=currentItem, timeLeft=str(remainingTime)[:-7], username=userName, bidList=bidList, ingredients=ingredientList)


@bp.route('/<id>/delete')
@login_required
def delete(id):
  currentItem = auctionListing.query.filter_by(id=id).first()
  if(current_user.id == currentItem.user_id):
    db.session.delete(currentItem)
    db.session.commit()
  return (redirect(url_for('main.profile')))

@bp.route('/<id>/watchlist')
@login_required
def watchlist(id):
  currentItem = auctionListing.query.filter_by(id=id).first()
  watchlistItems = Watchlist.query.filter_by(user_id=current_user.id)
  inWatchlist = False
  for item in watchlistItems:
    if(currentItem.id == item.item_id):
      inWatchlist = True
  if(inWatchlist == False):
    watchlistItem = Watchlist(item_id=currentItem.id, user_id=current_user.id, date_added=datetime.now(), total_bids=currentItem.total_bids, bid_status=currentItem.bid_status)
    db.session.add(watchlistItem)
    db.session.commit()
  return(redirect(url_for('main.watchlist')))

@bp.route('/sell', methods = ['GET','POST'])
@login_required
def sell():
    print('Method Type: ', request.method)
    form = ItemForm()
    if form.validate_on_submit():
        hoursPassed = form.duration.data
        hoursAdded = timedelta(hours = hoursPassed)
        db_file_path=check_upload_file(form)

        teaItem = auctionListing(user_id=current_user.id, start_time=datetime.now(), end_time=(datetime.now()+hoursAdded), starting_bid=form.startBid.data, current_bid=0,photos_url=db_file_path,description= form.description.data, weight=form.weight.data,title=form.title.data,tea_name=form.teaName.data,origin_country=form.country.data,oxidation=form.oxidation.data,packing=form.packingType.data,bid_status=1,total_bids=0)
        db.session.add(teaItem)
        db.session.commit()
        return redirect(str(teaItem.id))
    return render_template('items/listItem.html', form=form)