#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~
    Application-wide configurations.
    You can put whatever you want here. The convention is to write configuration
    variables in upper-case.

    :see http://flask.pocoo.org/docs/config/
    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    SECURITY_PASSWORD_SALT = 'my_darkness_moments_medt'
    APP_NAME = "Flask Skeleton"
    DEBUG = True
    CACHE_TIMEOUT = 60 * 60 * 15
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    UPLOAD_FOLDER = './app/tmp_files'
    ALLOWED_EXTENSIONS = {
        "application/pdf": "pdf",
        "application/msword": "doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "application/vnd.ms-excel": "xls",
        "application/excel": "xls",
        "application/x-excel": "xls",
        "application/x-msexcel": "xls",
        "text/plain": "txt",
        "image/jpeg": "jpg",
        "image/pjpeg": "jpeg",
        "image/png": "png"
    }

    COMPRESS_MIMETYPES = [
        'text/html',
        'text/css',
        'text/xml',
        'application/json',
        'application/javascript'
    ]

    PAGE = 1
    PER_PAGE = 99999999
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    print(os.path.join(basedir, 'dev.sqlite'))
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/kauemendes/www/test/ingresse/dev.sqlite'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    DEBUG_TB_ENABLED = True


class DevelopmentContainerConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev_container.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """Testing configuration."""

    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'testing.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class HomologConfig(BaseConfig):
    """Testing configuration."""

    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'homolog.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""

    print(os.path.join(basedir, 'prod.sqlite'))
    SECRET_KEY = 'my_prod_config_master'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////data/prod.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

