from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db

class Credential(db.Model):
    # Here we use a GUID to represent a credential
    id = db.Column(db.String, primary_key=True, nullable=False)
    # "password", "federated" and "public-key"
    type = db.Column(db.String, nullable=False)