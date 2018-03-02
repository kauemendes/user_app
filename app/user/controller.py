#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from flask import url_for

from app import db, g
from app.helper_kit.response_kit import ResponseReturnKit
from app.helper_kit.string_kit import StringKit
from app.helper_kit.validate_kit import ValidateKit
from app.user.model import User


class UserController(object):
    
    @staticmethod
    def save_new_user(json_body):

        username = json_body.get("username")
        email = json_body.get("email")
        password = json_body.get("password")
        password_confirm = json_body.get("password_confirm")

        if not username or not password or not password_confirm:
            return ResponseReturnKit.error400("Required field missing")

        if any(list(StringKit.password_check(password).values())):
            return ResponseReturnKit.error400("""A password is considered strong if: 6 characters length or more and 1 digit or more and 1 symbol or more and 1 uppercase letter or more and 1 lowercase letter or more""")

        if password_confirm != password:
            return ResponseReturnKit.error400("Password is not matching")

        find_user = User.query.filter_by(username=username).first()
        if find_user and not find_user.confirmed:
            return ResponseReturnKit.error400("User already exists")

        if find_user and find_user.confirmed:
            return ResponseReturnKit.error400("User or password invalid")

        if not ValidateKit.validate_email(email):
            return ResponseReturnKit.error400("Email is invalid")

        user = User(username=username)
        if email:
            user.email = email
        user.hash_password(password)
        user.registered_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()

        token = StringKit.generate_confirmation_token(user.username)
        confirm_url = url_for('confirm_email', token=token, _external=True)

        return {"url": confirm_url}, 201

    @staticmethod
    def get_user():
        user = g.user
        if user.confirmed:
            return user.serialize

        return ResponseReturnKit.error400("User not confirmed")

    @staticmethod
    def update_user(json_body):

        user = g.user

        if not user.confirmed:
            return ResponseReturnKit.error400("User not confirmed")

        if json_body.get("username"):
            user.username = json_body.get("username")
        if json_body.get("name"):
            user.name = json_body.get("name")
        if json_body.get("last_name"):
            user.last_name = json_body.get("last_name")
        if json_body.get("email"):
            if not ValidateKit.validate_email(json_body.get("email")):
                return ResponseReturnKit.error400("Email is invalid")
            user.email = json_body.get("email")

        db.session.commit()

        return user.serialize, 200

    @staticmethod
    def delete_user():
        user = g.user
        if user.confirmed:
            db.session.delete(user)
            db.session.commit()
            return {"msg": "deleted"}

        return ResponseReturnKit.error400("User not confirmed")


