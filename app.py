import json
import os
import datetime
from flask import Flask, session, render_template, g, url_for, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

from config import *
from util import *
from db import db
from models.user import User
app = Flask(__name__, static_url_path='/assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
    os.path.join(os.path.dirname(os.path.abspath(__name__)), 'webauthn.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = secret_key
"""
Functions for serving from template
"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/forgetpw/')
def forgetpw():
    return render_template('forgetpw.html')


"""
/getPubKeyCredParams
This function is for fetching pubKeyCredParams from server
Check MDN https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredentialCreationOptions/pubKeyCredParams
"""


@app.route('/getPubKeyCredParams')
def get_pubkey_credparams():
    return json.dumps(pubkey_credparams)


@app.route('/webauthn_begin_activate', methods=['POST'])
def webauthn_begin_activate():
    name = request.form.get('name')
    display_name = request.form.get('display_name')
    if not validate_name(name):
        return make_response(
            jsonify({
                "status": "failed",
                "msg": "Input error(name)"
            }), 401)
    if not validate_displayname(display_name):
        return make_response(
            jsonify({
                "status": "failed",
                "msg": "Input error(display_name)"
            }), 401)
    if User.query.filter_by(email=name).first():
        return make_response(
            jsonify({
                "status": "failed",
                "msg": "User alreday exists"
            }), 401)
    session['register_username'] = name
    session['register_display_name'] = display_name
    session['register_ukey'] = generate_ukey()
    session['challenge'] = generate_challenge(32).rstrip('=')
    return jsonify({
        "status": "success",
        "publicKey": {
            "rp": rp,
            "user": {
                "id": session['register_ukey'],
                "name": name,
                "displayName": display_name
            },
            "pubKeyCredParams": pubkey_credparams,
            "challenge": session['challenge']
        }
    })


@app.route('/makeCredential/<string:email>')
def make_credential(email: str):
    return email


if __name__ == '__main__':
    app.run()