import datetime

from app import db

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

#class User(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  username = db.Column(db.String(50), unique=True, nullable=False)

class UserMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jauge_i = db.Column(db.Integer, nullable=False, default=0)
    jauge_r = db.Column(db.Integer, nullable=False, default=0)
    jauge_c = db.Column(db.Integer, nullable=False, default=0)
    jauge_4 = db.Column(db.Integer, nullable=False, default=0)