import datetime

from app import db

from sqlalchemy import Boolean, DateTime, Integer, String

class UserMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jauge_i = db.Column(db.Integer, nullable=False, default=0)
    jauge_r = db.Column(db.Integer, nullable=False, default=0)
    jauge_c = db.Column(db.Integer, nullable=False, default=0)
    jauge_4 = db.Column(db.Integer, nullable=False, default=0)
    air_defense = db.Column(db.Integer, nullable=False, default=0)
    water_defense = db.Column(db.Integer, nullable=False, default=0)
    fire_defense = db.Column(db.Integer, nullable=False, default=0)
    earth_defense = db.Column(db.Integer, nullable=False, default=0)