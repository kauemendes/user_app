#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.models.user
    ~~~~~~~~~~~~~~~
    The User model.

"""
import datetime
import json

from app import app, db
from sqlalchemy.dialects.mysql import LONGTEXT
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(255), index=True, unique=True)

    name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    email = db.Column(db.String(255), index=True)
    phone = db.Column(db.String(255), index=False)

    password_hash = db.Column(db.String(120))

    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    updated_at = db.Column(db.TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    registered_on = db.Column(db.DateTime, nullable=False)

    app_preferences = db.Column(db.Text, nullable=True)

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=1200):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {"user_id": self.id,
                "username": self.username,
                "name": self.name,
                "last_name": self.last_name,
                "email": self.email,
                "preferences": self.app_preferences
                }

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["id"])
        return user
