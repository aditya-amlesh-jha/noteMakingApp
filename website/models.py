from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# UserMixin is a class that contains default implementations for the methods that Flask-Login expects user objects to
# have.

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(150))
    content = db.Column(db.String(30000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    aadhar = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')
