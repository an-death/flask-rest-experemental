from app import api
from resources import BooksList, BookDescription, Calculate, TransResult

api.add_resource(BooksList, '/books', endpoint='books')
api.add_resource(BookDescription, '/book/<string:ISBN>', endpoint='book')
api.add_resource(Calculate, '/calculate', endpoint='calculate')
api.add_resource(TransResult, '/transaction/<string:hash>', endpoint='transaction')
