from flask_restful import (
    Resource,
    reqparse,
    request
)

from app import auth, g
from app.helper_kit.response_kit import ResponseReturnKit
from app.user.controller import UserController

parser = reqparse.RequestParser()

parser.add_argument('message', type=str, help='Name to filter')


class UserResource(Resource):

    def post(self):
        if not request.json:
            return ResponseReturnKit.error400("empty json")

        try:
            return UserController.save_new_user(request.json)
        except Exception as e:
            return ResponseReturnKit.error400(str(e))

    @auth.login_required
    def get(self):
        return UserController.get_user()

    @auth.login_required
    def put(self):
        if not request.json:
            return ResponseReturnKit.error400("empty json")

        try:
            return UserController.update_user(request.json)
        except Exception as e:
            return ResponseReturnKit.error400((str(e)))


    @auth.login_required
    def delete(self):
        try:
            return UserController.delete_user()
        except Exception as e:
            return ResponseReturnKit.error400((str(e)))
