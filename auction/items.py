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


# Image upload function
def check_upload_file(form):
  fp=form.photos.data
  filename=fp.filename
  BASE_PATH=os.path.dirname(__file__)

  upload_path=os.path.join(BASE_PATH,'static/image/itemImages/',secure_filename(filename))
  db_upload_path='/static/image/itemImages/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

# specific item page
@bp.route('/<int:id>', methods = ['GET','POST'])
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
    form = BidForm()
    # Holds whether or not the person has this item within their watchlist
    watchlistExists = False
    if (current_user.is_authenticated):

        if (current_user.id == currentItem.user_id):

            bidList = Bid.query.filter_by(listing_id = currentItem.id).order_by(desc(Bid.bid_time))
        else:
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

        # If the item is in the person's watchlist, do not show the button
        if (Watchlist.query.filter_by(user_id=current_user.id).filter_by(item_id=id).first()):
          watchlistExists = True
    
    # compile ingredient list
    ingredientList = currentItem.tea_name.split(',')

    form = BidForm()

    return render_template('items/details.html', form=form, auctionListing=currentItem, timeLeft=str(remainingTime)[:-7], username=userName, bidList=bidList, ingredients=ingredientList, watchlistExists = watchlistExists)



# Item delete function
@bp.route('/<int:id>/delete')
@login_required
def delete(id):
  # Query the current item
  currentItem = auctionListing.query.filter_by(id=id).first()
  # Delete the item if the user who added the item is the same as the logged in user
  if(current_user.id == currentItem.user_id):
    db.session.delete(currentItem)
    db.session.commit()
  # Return to the homepage
  return (redirect(url_for('main.profile')))


# User Watchlist page function
@bp.route('/<int:id>/watchlist')
@login_required
def watchlist(id):
  # Queries to store information on the currentntly viewing item and the items in the watchlist
  currentItem = auctionListing.query.filter_by(id=id).first()
  watchlistItems = Watchlist.query.filter_by(user_id=current_user.id)
  inWatchlist = False

  # Checking if the current item matches items in the the watchlist
  for item in watchlistItems:
    if(currentItem.id == item.item_id):
      inWatchlist = True
  
  # Add the current item to the watchlist if it is not already there
  if(inWatchlist == False):
    watchlistItem = Watchlist(item_id=currentItem.id, user_id=current_user.id, date_added=datetime.now(), total_bids=currentItem.total_bids, bid_status=currentItem.bid_status)
    db.session.add(watchlistItem)
    db.session.commit()

  # Send the user the the watchlist
  return(redirect(url_for('main.watchlist')))


# Remove from watchlist function
@bp.route('/watchlist/remove/<int:id>')
@login_required
def remove(id):
  # Queries the current item from the watchlist
  watchlistItem = Watchlist.query.filter_by(user_id=current_user.id).filter_by(item_id=id).first()

  db.session.delete(watchlistItem)
  db.session.commit()
  # Send the user the the watchlist
  return(redirect(url_for('main.watchlist')))


# Sell Item page function
@bp.route('/sell', methods = ['GET','POST'])
@login_required
def sell():
    # Generate form to input information
    print('Method Type: ', request.method)
    form = ItemForm()

    # Run upon checking the submission is valid
    if form.validate_on_submit():
      # Store infomation to generate the end time of the bid
        hoursPassed = form.duration.data
        hoursAdded = timedelta(hours = hoursPassed)
        # Store the file path for the uploaded item image
        db_file_path=check_upload_file(form)

        # Generate and add the data the the auctionListing table in the database
        teaItem = auctionListing(user_id=current_user.id, start_time=datetime.now(), end_time=(datetime.now()+hoursAdded), starting_bid=form.startBid.data, current_bid=0,photos_url=db_file_path,description= form.description.data, weight=form.weight.data,title=form.title.data,tea_name=form.teaName.data,origin_country=form.country.data,oxidation=form.oxidation.data,packing=form.packingType.data,bid_status=1,total_bids=0)
        db.session.add(teaItem)
        db.session.commit()

        # Send the user to the details page for the recently created item
        return redirect(str(teaItem.id))

    # Display the sell item form
    return render_template('items/listItem.html', form=form)
