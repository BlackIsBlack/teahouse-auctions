from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .forms import ItemForm
from .models import auctionListing, User
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

@bp.route('/<id>')
def display(id):
  try:
    currentItem = auctionListing.query.filter_by(id=id).first()
    remainingTime = (currentItem.end_time - datetime.now())
    if(remainingTime < timedelta(0)):
      currentItem.bid_status = 0
      db.session.commit()
    userName = User.query.filter_by(id=currentItem.user_id).first().username
    return render_template('items/details.html', auctionListing=currentItem, timeLeft=str(remainingTime)[:-7], username=userName)
  except:
    return render_template('errorpage.html')

@bp.route('/<id>/delete')
def delete(id):
  currentItem = auctionListing.query.filter_by(id=id).first()
  if(current_user.id == currentItem.user_id):
    db.session.delete(currentItem)
    db.session.commit()
  return (redirect(url_for('main.profile')))

@bp.route('/sell', methods = ['GET','POST'])
@login_required
def sell():
    print('Method Type: ', request.method)
    form = ItemForm()
    if form.validate_on_submit():
        hoursPassed = form.duration.data
        hoursAdded = timedelta(hours = hoursPassed)
        db_file_path=check_upload_file(form)

        teaItem = auctionListing(user_id=current_user.id, start_time=datetime.now(), end_time=(datetime.now()+hoursAdded), starting_bid=form.startBid.data, current_bid=0,photos_url=db_file_path,description= form.description.data, weight=form.weight.data,title=form.title.data,tea_name=form.teaName.data,origin_country=form.country.data,oxidation=form.oxidation.data,packing=form.packingType.data,bid_status=1,highest_bid=0,total_bids=0)
        db.session.add(teaItem)
        db.session.commit()
        return redirect(str(teaItem.id))
    return render_template('items/listItem.html', form=form)
