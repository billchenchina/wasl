from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db

from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    display_name = db.Column(db.String, nullable=False)
