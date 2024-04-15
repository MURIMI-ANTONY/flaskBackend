from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),nullable=False,unique=True)
    first_name = db.Column(db.String())
    second_name = db.Column(db.String())
    password=db.Column(db.String)
    notes = db.relationship('Note' ,backref='user')

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))