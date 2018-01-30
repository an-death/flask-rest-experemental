import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter

from config import Dev, Ops

app = Flask(__name__)
if os.environ.get('LOCATION') == "OPS":
    app.secret_key = Ops.SECRET_KEY
    app.config.from_object(Ops)
else:
    app.secret_key = Dev.SECRET_KEY
    app.config.from_object(Dev)


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(app.config['LOG_FILE'], 'a', 1 * 1024 ** 3, 3)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.info('flask_rest started')

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

db = SQLAlchemy(app)
api = Api(app=app, catch_all_404s=True)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter

from resources import BooksList, BookDescription, Calculate, TransResult

api.add_resource(BookDescription, '/books/<id>', endpoint='book')
api.add_resource(BooksList, '/books', endpoint='books')
api.add_resource(Calculate, '/calculate', endpoint='calculate')
api.add_resource(TransResult, '/transaction/<hash_id>')
