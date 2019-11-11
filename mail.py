import os
import random
import string
import json
from datetime import datetime
# import sqlite3
# from sqlite3 import Error
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import mailgun 


app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'master.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(200))
    username = db.Column(db.String(80), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created = db.Column(db.String(80), nullable=False)
    updated = db.Column(db.String(80))

    def __init__(self, username, alias, active, created, updated):
        self.username = username
        self.alias = alias
        self.active = active
        self.created = created
        self.updated = updated


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'alias', 'active', 'created', 'updated')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


def derive_username():
    # chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    username_chars = '._'
    random.seed = (os.urandom(1024))

    first_names = json.loads(open('fname.json').read())
    last_names = json.loads(open('lname.json').read())

    name_extra = ''.join(random.choice(string.digits))
    name = random.choice(first_names) + random.choice(username_chars) + \
        random.choice(last_names) + name_extra

    return name.lower()


# error handler
@app.errorhandler(404)
def not_found(e):
    api_status = {"success": False}
    return jsonify(api_status)

# endpoint to create new user
@app.route('/tempmail/v1/user', methods=['POST'])
@cross_origin(allow_headers=['*'], origins=['*'])
def add_user():
    username = derive_username()
    created = datetime.now()
    updated = created
    alias = request.json['alias']
    active = request.json['active']

    new_user = User(username, alias, active, created, updated)

    db.session.add(new_user)
    db.session.commit()

    mg = mailgun.MailGun('add', username)
    r = mg.update_fwd_route(mg.operation, mg.username)

    return user_schema.jsonify(new_user)


# endpoint to show all users
@app.route("/tempmail/v1/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    result.sort(key=sort_by_key, reverse=True)
    return jsonify(result)


def sort_by_key(val):
    return val['id']


# endpoint to get user detail by id
@app.route("/tempmail/v1/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/tempmail/v1/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    old_active_status = user.active
    username = user.username
    new_active_status = request.json['active']
    updated = datetime.now()

    user.active = new_active_status
    user.updated = updated

    db.session.commit()

    # adding the username to the relevant list when the status is toggled
    if old_active_status == True and  new_active_status == False:
        # dropping the user
        mg = mailgun.MailGun('', username)
        mg.update_fwd_route("del", mg.username)
        mg.update_drop_route("add", mg.username)
    elif old_active_status == False and new_active_status == True:
        # fwding the user
        mg = mailgun.MailGun('', username)
        mg.update_drop_route("del", mg.username)
        mg.update_fwd_route("add", mg.username)

    return user_schema.jsonify(user)


if __name__ == "__main__":
    app.run(debug=True)
