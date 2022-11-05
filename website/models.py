
from datetime import datetime
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),index=True,unique=True,nullable=False)
    email = db.Column(db.String(100),index=True,nullable=False)
    contact_number = db.Column(db.String(15),index=True,nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    
    comments = db.relationship('Comment',backref='user')

class Concert(db.Model):
    __tablename__ = "concerts"
    id = db.Column(db.Integer, primary_key=True)
    event_creator = db.Column(db.String(100))
    event_name = db.Column(db.String(80))
    event_description = db.Column(db.String(200))
    event_date= db.Column(db.Date)
    event_genre = db.Column(db.String(100))
    event_venue = db.Column(db.String(100))
    ticket_count = db.Column(db.Integer)
    ticket_price = db.Column(db.Integer)
    event_status = db.Column(db.String(30))
    event_image = db.Column(db.String(400))

    comments = db.relationship('Comment',backref='concert')

    def __repr__(self):
        return "<Name: {}>".format(self.name)


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer,primary_key=True)
    event_id = db.Column(db.Integer) # Foreign key
    ticket_owner = db.Column(db.String(100))
    ticket_quantity = db.Column(db.Integer)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(400))
    created = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)