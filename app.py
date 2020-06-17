import json
import os
import datetime
from flask import Flask, session, render_template, g, url_for, request, jsonify, make_response, redirect
from flask_sqlalchemy import SQLAlchemy

from config import *
from util import *
from db import db
from models.user import User
from models.publickeycredential import PublicKeyCredential

import webauthn

from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

app = Flask(__name__, static_url_path='/assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
    os.path.join(os.path.dirname(os.path.abspath(__name__)), 'webauthn.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = secret_key
"""
Functions for serving from template
"""

@login_manager.user_loader
def load_user(user_id):
    try:
        int(user_id)
    except ValueError:
        return None

    return User.query.get(int(user_id))

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
    if User.query.filter_by(email=name).first():
        return make_response(
            jsonify({
                "status": "failed",
                "msg": "User already exists."
            }), 401)
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


@app.route('/verify_credential_info', methods=["POST"])
def verify_credential_info():
    name = session['register_username']
    display_name = session['register_display_name']
    ukey = session['register_ukey']
    challenge = session['challenge']
    registration_response = request.form
    webauthn_registration_response = webauthn.WebAuthnRegistrationResponse(
        rp["id"],
        request.host_url[:-1], # This aims to remove the ending slash
        registration_response,
        challenge,
        self_attestation_permitted=True,
        none_attestation_permitted=True)
    try:
        webauthn_credential = webauthn_registration_response.verify()
    except Exception as e:
        return make_response(jsonify({"status": "failed", "msg": str(e)}), 401)
    if PublicKeyCredential.query.filter_by(
            credential_id=webauthn_credential.credential_id).first():
        return make_response(
            jsonify({
                "status": "failed",
                "msg": "Key already exists."
            }), 401)
    if User.query.filter_by(email=name).first():
        return make_response(
            jsonify({
                "status": "failed",
                "msg": "User already exists."
            }), 401)

    webauthn_credential.credential_id = str(webauthn_credential.credential_id,
                                            "utf-8")
    webauthn_credential.public_key = str(webauthn_credential.public_key,
                                         "utf-8")
    user = User(display_name=display_name, email=name)
    db.session.add(user)
    publickey_redential = PublicKeyCredential(
        ukey=ukey,
        credential_id=webauthn_credential.credential_id,
        pub_key=webauthn_credential.public_key,
        rp_id=rp["id"],
        email=name,
        user=user)
    db.session.add(publickey_redential)
    db.session.commit()
    login_user(user)
    return make_response(jsonify({"status": "success"}))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='test.com', port=8443, ssl_context='adhoc')