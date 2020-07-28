from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'))
    items = db.relationship('Item', backref='author_item', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_home_id(self, id):
        self.home_id = id

    def get_items(self):
        home_users = User.query.filter_by(home_id=self.home_id)
        home_users_ids = [x.id for x in home_users]
        return Item.query.filter(Item.user_id.in_(home_users_ids))


    def __repr__(self):
        return '<User {}>'.format(self.username)


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_name = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    users = db.relationship('User', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Home {}>'.format(self.home_name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(128))
    amount = db.Column(db.String(60))
    note = db.Column(db.String(256))
    bought = db.Column(db.Boolean)