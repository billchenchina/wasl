from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    display_name = db.Column(db.String, nullable=False)
