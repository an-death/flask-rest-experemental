import os

import database


class Configuration:
    # add global config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    LOG_FILE = 'flask_rest.log'
    DEBUG = os.environ.get('DEBUG', 'on') == 'on'
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))


class Dev(Configuration):
    SECRET_KEY = 'some_simple_key'
    SQLALCHEMY_DATABASE_URI = database.Dev.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_BINDS = database.Dev.SQLALCHEMY_BINDS
    SERVER_HOST = 'localhost'
    SERVER_PORT = 8001


class Ops(Configuration):
    pass  # some specific db configs for product
