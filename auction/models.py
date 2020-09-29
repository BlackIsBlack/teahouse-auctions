from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index=True, unique= True, nullable=False)
    emailId = db.Column(db.String(100), index = True, nullable = False)
    password_hash = db.Column(db.String(255),nullable=False)

    comments = db.relationship('Comment', backref='user')