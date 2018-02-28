# -*- coding: utf-8 -*-
import urllib.request


from flask import json
from flask_testing import TestCase
from app import app, db, confirm_email, get_auth_token
from app.helper_kit.json_kit import JsonKit
from app.user.model import User


class TestUser(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def create_data(self):
        user = User()
        user.username = "userteste"
        user.name = "User"
        user.last_name = "Teste"
        user.hash_password("123456")
        user.confirmed_on = True
        db.session.add(user)
        db.session.commit()

    def test_user_with_missing_fields(self):
        response = self.client.post('/v1/user',
                                    content_type='application/json',
                                    data=json.dumps(
                                        {
                                            "username": "userteste2",
                                            "email": "usertest",
                                            "password": "@cC1234567"
                                        }
                                    ))

        self.assertEqual(response.status_code, 400)

    def test_user_with_wrong_email(self):
        response = self.client.post('/v1/user',
                                    content_type='application/json',
                                    data=json.dumps(
                                        {
                                            "username": "userteste2",
                                            "email": "usertest",
                                            "password": "@cC1234567",
                                            "password_confirm": "@cC1234567"
                                        }
                                    ))

        self.assertEqual(response.status_code, 400)

    def test_user_wrong_password(self):
        response = self.client.post('/v1/user',
                                    content_type='application/json',
                                    data=json.dumps(
                                        {
                                            "username": "userteste2",
                                            "email": "userteste@userteste.com",
                                            "password": "@cC1234567",
                                            "password_confirm": "@dwasada"
                                        }
                                    ))

        self.assertEqual(response.status_code, 400)

    def test_user_register_perfect_scenario(self):
        response = self.client.post('/v1/user',
                                    content_type='application/json',
                                    data=json.dumps(
                                        {
                                            "username": "userteste2",
                                            "email": "userteste@userteste.com",
                                            "password": "@cC1234567",
                                            "password_confirm": "@cC1234567"
                                        }
                                    ))

        self.assertEqual(response.status_code, 201)
        self.assertIn('url', response.json)

    def test_user_confirm_email(self):
        response = self.client.post('/v1/user',
                                    content_type='application/json',
                                    data=json.dumps(
                                        {
                                            "username": "userteste2",
                                            "email": "userteste@userteste.com",
                                            "password": "@cC1234567",
                                            "password_confirm": "@cC1234567"
                                        }
                                    ))

        self.assertEqual(response.status_code, 201)
        self.assertIn('url', response.json)
        url = response.json.get('url').split("/")
        resp = confirm_email(url[6])
        self.assertIn("confirmado", resp.split(" "))

        return True

    def test_get_token_for_user(self):
        lOk = self.test_user_confirm_email()

        if lOk:
            user = User.query.filter_by(username="userteste2").first()
            token = user.generate_auth_token()
            token = token.decode('ascii')
            self.assertTrue(token)

            return token

    def test_get_user_info(self):
        token = self.test_get_token_for_user()

        if token:
            headers = {
                'Authorization': 'Basic dXNlcnRlc3RlMjpAY0MxMjM0NTY3'
            }
            response = self.client.get("/v1/user", headers=headers)
            self.assert200(response)
            self.assertIn("username", response.json)
            self.assertIn("name", response.json)
            self.assertIn("last_name", response.json)
            self.assertIn("email", response.json)

    def test_update_user_information_name(self):
        token = self.test_get_token_for_user()

        if token:
            headers = {
                'Authorization': 'Basic dXNlcnRlc3RlMjpAY0MxMjM0NTY3'
            }
            response = self.client.put("/v1/user",
                                       content_type="application/json",
                                       headers=headers,
                                       data=json.dumps({
                                           "name": "Carlos"
                                       }))
            self.assert200(response)
            user = User.query.filter_by(username="userteste2").first()
            self.assertEqual("Carlos", user.name)

    def test_update_user_information_last_name(self):
        token = self.test_get_token_for_user()

        if token:
            headers = {
                'Authorization': 'Basic dXNlcnRlc3RlMjpAY0MxMjM0NTY3'
            }
            response = self.client.put("/v1/user",
                                       content_type="application/json",
                                       headers=headers,
                                       data=json.dumps({
                                           "last_name": "Pereira"
                                       }))
            self.assert200(response)
            user = User.query.filter_by(username="userteste2").first()
            self.assertEqual("Pereira", user.last_name)

    def test_update_user_information_wrong_email(self):
        token = self.test_get_token_for_user()

        if token:
            headers = {
                'Authorization': 'Basic dXNlcnRlc3RlMjpAY0MxMjM0NTY3'
            }
            response = self.client.put("/v1/user",
                                       content_type="application/json",
                                       headers=headers,
                                       data=json.dumps({
                                           "email": "djwahi"
                                       }))
            self.assert400(response)

    def test_update_user_information_correct_email(self):
        token = self.test_get_token_for_user()

        if token:
            headers = {
                'Authorization': 'Basic dXNlcnRlc3RlMjpAY0MxMjM0NTY3'
            }
            response = self.client.put("/v1/user",
                                       content_type="application/json",
                                       headers=headers,
                                       data=json.dumps({
                                           "email": "carlos@gmail.com"
                                       }))
            self.assert200(response)
            user = User.query.filter_by(username="userteste2").first()
            self.assertEqual("carlos@gmail.com", user.email)

    def test_delete_user(self):
        token = self.test_get_token_for_user()

        if token:
            headers = {
                'Authorization': 'Basic dXNlcnRlc3RlMjpAY0MxMjM0NTY3'
            }
            response = self.client.delete("/v1/user", headers=headers)
            self.assert200(response)
