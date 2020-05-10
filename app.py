from flask import Flask, render_template, g, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__, static_url_path='/assets')
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://test.db"
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/register/')
def register():
    return render_template('register.html')

app.run()