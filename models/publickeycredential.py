from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db
from models.credential import Credential

class PublicKeyCredential(Credential):
    rawid = db.Column(db.)