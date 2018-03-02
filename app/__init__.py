#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import datetime
from flask_httpauth import HTTPBasicAuth

from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, render_template, render_template_string, g
from flask_restful import Api

from flask_restful_swagger import swagger
from flask_cors import CORS

from werkzeug.contrib.cache import SimpleCache
from flask.ext.sqlalchemy import SQLAlchemy
from flask_compress import Compress
from flask_cache import Cache

# Initialize a developmentConfig in case of APP_SETTINGS not provided

app_settings = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')

app = Flask(__name__, template_folder='templates', static_folder='templates/static')
Compress(app)

# create multiple sqlalchemy engines
db = SQLAlchemy(app)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# set config parameters
app.config.from_object(app_settings)

# auth basic
auth = HTTPBasicAuth()

# Compress Extenstion
Compress(app)

# Cors - Multiples Origins HEADERS
cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

# OAuth2 Server Provider
# from app.services_legacy.authorization_server import create_server
# OAuth2 Initialize Application
# app, oauth = create_server(app)

# Simple Cache if Needed
cache = SimpleCache(__name__)

# Bcrypt into APP
bcrypt = Bcrypt(app)

# Initialize API APP
api = swagger.docs(Api(app),
                   apiVersion='1.2.0.0',
                   produces=[
                       "application/json",
                       "text/html",
                       "multipart/form-data",
                       "audio/ogg",
                       "application/msgpack"
                   ])


from app.utils import prepare_json_response

# Inicia as rotas da api
from app import urls
urls.StartApi(api)


@auth.verify_password
def verify_password(username_or_token, password):
    from app.user.model import User
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/v1/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/v1/user/confirm/<token>')
def confirm_email(token):
    from app.helper_kit.string_kit import StringKit
    from app.helper_kit.response_kit import ResponseReturnKit
    from app.user.model import User

    try:
        username = StringKit.confirm_token(token)
    except Exception as e:
        ResponseReturnKit.error400('The confirmation link is invalid or has expired.')

    user = User.query.filter_by(username=username).first_or_404()
    if user:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.commit()

    return render_template_string(
        """
        <html>
            <body>
                E-mail confirmado para o usuário %s
            </body>
        </html>
        """ % user.username
    )

@app.route("/help", methods=["GET"])
def help():
    """
    Returns a list of available URLs.

    :returns: A JSON response object
    :rtype: flask.Response
    """
    # func_list = {}
    func_list = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != "static":
            func_list.append(rule.rule)

    return jsonify(
        prepare_json_response(
            message="All URL endpoints",
            success=True,
            data=func_list
        )
    )

# -- Error handlers
# Override the default handlers with JSON responses
@app.errorhandler(400)
def forbidden(error):
    """
    Renders 400 response
    :returns: JSON
    :rtype: flask.Response
    """
    if not error.description:
        error.description = "Error 400: Bad request"

    return jsonify(
        prepare_json_response(
            message=error.description,
            success=False,
            data=None
        )
    ), 400


@app.errorhandler(401)
def forbidden(error):
    """
    Renders 400 response
    :returns: JSON
    :rtype: flask.Response
    """

    if not error.description:
        error.description = "Error 401: Unauthorized"

    return jsonify(
        prepare_json_response(
            message=error.description,
            success=False,
            data=None
        )
    ), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Renders 403 response
    :returns: JSON
    :rtype: flask.Response
    """

    if not error.description:
        error.description = "Error 403: Forbidden"

    return jsonify(
        prepare_json_response(
            message=error.description,
            success=False,
            data=None
        )
    ), 403


@app.errorhandler(404)
def not_found(error):
    """
    Renders 404 response
    :returns: JSON
    :rtype: flask.Response
    """
    if not error.description:
        error.description = "Error 404: Not Found"

    return jsonify(
        prepare_json_response(
            message=error.description,
            success=False,
            data=None
        )
    ), 404


@app.errorhandler(405)
def not_found(error):
    """
    Renders 405 response
    :returns: JSON
    :rtype: flask.Response
    """
    if not error.description:
        error.description = "Error 405: Method not allowed"

    return jsonify(
        prepare_json_response(
            message=error.description,
            success=False,
            data=None
        )
    ), 405


@app.errorhandler(500)
def internal_server_error(error):
    """
    Renders 500 response
    :returns: JSON
    :rtype: flask.Response
    """
    if not error.description:
        error.description = "Error 500: Internal server error"

    return jsonify(
        prepare_json_response(
            message=error.description,
            success=False,
            data=None
        )
    ), 405
