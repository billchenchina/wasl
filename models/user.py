from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db


class User(SQLAlchemy.Model):
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)

    def __init__(cls, classname, bases, dict_):
        super().__init__(classname, bases, dict_)
