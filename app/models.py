from flask_login import UserMixin
from datetime import datetime
from app import db


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  name = db.Column(db.String(300), nullable=False)
  password = db.Column(db.String(100), nullable=False)

  def __repr__(self):
    return('<User %r>' % (self.username))