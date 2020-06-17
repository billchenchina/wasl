from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db

class PublicKeyCredential(db.Model):
    ukey = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    credential_id = db.Column(db.String(250), unique=True, nullable=False)
    pub_key = db.Column(db.String(65), unique=True, nullable=True)
    rp_id = db.Column(db.String(253), nullable=False)
    email = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    user = db.relationship('User', backref = db.backref('publickeys', lazy='dynamic'))