# -*- coding: utf-8 -*-

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    phonenum = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    commodity = db.relationship('Commodity', backref='author', lazy='dynamic')
    comment = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<id %d, username %r, phonenum %r>" % (self.id, self.username, self.phonenum)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Commodity(db.Model):
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64))
    description = db.Column(db.Text())
    price = db.Column(db.Integer())

    discount = db.Column(db.Integer())
    location = db.Column(db.String(32))
    type = db.Column(db.String(32))

    wechatnum = db.Column(db.String(32))
    qqnum = db.Column(db.String(32))
    image = db.Column(db.String(64))

    status = db.Column(db.Integer())
    clitime = db.Column(db.Integer(), default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='commodity', lazy='dynamic')

    def __repr__(self):
        return "<id %d, name %r>" % (self.id, self.name)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))