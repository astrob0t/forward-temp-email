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


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'crud.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(200))
    username = db.Column(db.String(80), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created = db.Column(db.String(80), nullable=False)
    updated = db.Column(db.String(80), nullable=False)

    def __init__(self, id, username, alias, active, created, updated):
        self.id = id
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

    # print(name.lower())
    return name.lower()


# endpoint to create new user
@app.route('/v1/user', methods=['POST'])
def add_user():
    username = derive_username()
    created = datetime.now()
    alias = request.json['alias']
    active = request.json['active']

    new_user = User(username, alias, active, created)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# endpoint to show all users
@app.route("/v1/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


# endpoint to get user detail by id
@app.route("/v1/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/v1/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    active = request.json['active']
    updated = datetime.now()

    user.active = active
    user.updated = updated

    db.session.commit()
    return user_schema.jsonify(user)



if __name__ == "__main__":
    app.run(debug=True)
