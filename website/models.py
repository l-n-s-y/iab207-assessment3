
from datetime import datetime
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),index=True,unique=True,nullable=False)
    emailid = db.Column(db.String(100),index=True,nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    #comments = db.relationship('Comment',backref='user')

class Concert(db.Model):
    __tablename__ = "concerts"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80))
    event_description = db.Column(db.String(200))
    event_date= db.Column(db.Date)
    event_genre = db.Column(db.String(100))
    event_venue = db.Column(db.String(100))
    ticket_count = db.Column(db.Integer)
    ticket_price = db.Column(db.Integer)
    event_image = db.Column(db.String(400))

    #comments = db.relationship('Comment',backref='concert')

    def __repr__(self):
        return "<Name: {}>".format(self.name)


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer,primary_key=True)
    event_id = db.Column(db.Integer) # Foreign key
    ticket_owner = db.Column(db.String(100))
    ticket_quantity = db.Column(db.Integer)
