from flask_login import UserMixin
from .__init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    balance = db.Column(db.FLOAT())
    loginCount = db.Column(db.Integer())
    loginFailCount = db.Column(db.Integer())
    resetCount = db.Column(db.Integer())