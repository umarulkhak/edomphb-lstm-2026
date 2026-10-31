# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

import os
from os import environ
from urllib.parse import quote_plus

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    APP_VERSION = '2026.1.0'

    SECRET_KEY = environ.get('SECRET_KEY', 'development-key-change-before-deploying')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

    # For 'in memory' database, please use:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
            
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # THEME SUPPORT
    #  if set then url_for('static', filename='', theme='')
    #  will add the theme name to the static URL:
    #    /static/<DEFAULT_THEME>/filename
    # DEFAULT_THEME = "themes/dark"
    DEFAULT_THEME = None


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = environ.get('SECRET_KEY')

    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        database_user = environ.get('APPSEED_DATABASE_USER')
        database_password = environ.get('APPSEED_DATABASE_PASSWORD')
        database_host = environ.get('APPSEED_DATABASE_HOST')
        database_name = environ.get('APPSEED_DATABASE_NAME')
        database_port = environ.get('APPSEED_DATABASE_PORT', '5432')
        if all((database_user, database_password, database_host, database_name)):
            SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
                quote_plus(database_user),
                quote_plus(database_password),
                database_host,
                database_port,
                quote_plus(database_name),
            )


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
