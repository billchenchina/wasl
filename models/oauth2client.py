from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db


class OAuth2Client(db.Model):
    __tablename__ = 'oauth2_client'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
                                                  ondelete='CASCADE'))
    user = db.relationship('User')

