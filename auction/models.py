from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), index=True, unique= True, nullable=False)
    email = db.Column(db.String(100), index = True, nullable = False)
    password_hash = db.Column(db.String(255),nullable=False)
    contact_number = db.Column(db.String(20), unique = True)
    address = db.Column(db.String(200), nullable=False)

class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_added =  db.Column(db.DateTime, default=datetime.now(), nullable=False)
    total_bids = db.Column(db.Integer, db.ForeignKey('auctionListing.total_bids'), nullable=False)
    bid_status = db.Column(db.Integer, db.ForeignKey('auctionListing.bid_status'), nullable=False)
    highest_bid = db.Column(db.Float, nullable=False)

class Bid(db.Model):
    __tablename__ = 'bid'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    listing_id = db.Column(db.Integer, db.ForeignKey('auctionListing.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bid_amount = db.Column(db.Float, nullable=False)
    bid_time = db.Column(db.DateTime, default=datetime.now())
    bid_status = db.Column(db.Integer, nullable = False)

class auctionListing(db.Model):
    __tablename__ = 'auctionListing'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    starting_bid = db.Column(db.Float, nullable=False) #make 0 minimum
    current_bid = db.Column(db.Float, nullable=False) #same as above
    photos_url = db.Column(db.String())
    description = db.Column(db.String(255))
    weight = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    tea_name = db.Column(db.String(60), nullable=False)
    origin_country = db.Column(db.String(60), nullable=False)
    oxidation = db.Column(db.String(60), nullable=False)
    packing = db.Column(db.String(60), nullable=False)
    bid_status = db.Column(db.Integer, nullable=False)
    total_bids = db.Column(db.Integer, nullable=False)
