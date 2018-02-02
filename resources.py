from flask import request
from flask_restful import Resource, fields, marshal_with, abort

from app import db
from models.models import Customer, Transaction, Books, Category
from parsers import get_parsers

book_fields = {
    'id': fields.Integer,
    'ISBN': fields.String,
    'category': fields.String,
    'cost': fields.Float,
    'currency': fields.Integer(attribute='currency_id')
}

book_fields_desc = book_fields.copy()
book_fields_desc['description'] = fields.String

calculate_fields = {
    'books': fields.List,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String(attribute='phone_number')
}
transaction_fields = {
    'hash_id': fields.String,
    'date': fields.DateTime,
    'total_cost': fields.Float,
    'currency': fields.Integer(attribute='currency_id')
    # 'books': fields.String
}

book_parser, calculate_parser, book_creater = get_parsers()


class BookDescription(Resource):
    @marshal_with(book_fields_desc)
    def get(self, id):
        book = Books.query.get(id)
        if not book:
            abort(404, message=f"Book with id <{id}> not found")
        return book

    @marshal_with(book_fields)
    def put(self, id):
        pass  # todo add if needed

    def delete(self, id):
        pass  # todo add if needed


class BooksList(Resource):
    @marshal_with(book_fields)
    def get(self):
        args = book_parser.parse_args()
        query = Books.query
        if args['category']:
            query = query.filter_by(category_id=Category.query.filter_by(name=args['category']).first().id)
        if args['cost_from']:
            query = query.filter(Books.cost >= args['cost_from'])
        if args['cost_to']:
            query = query.filter(Books.cost <= args['cost_to'])
        if args['cost']:
            query = query.filter(Books.cost == args['cost'])
        return query.all()

    def post(self):
        args = book_creater.parse_args()
        Books.add_book(ISBN=args['ISBN'], category=args['category'], cost=args['cost'], currency_id=args['currency_id'])
        return 201

class Calculate(Resource):
    # todo add calculation get and put method's for customize
    @marshal_with(transaction_fields)
    def post(self):
        books = []
        args = calculate_parser.parse_args()
        req = request.json['books']
        user = Customer.query.filter(Customer.email == args['email']).first()

        if not user:
            user = Customer(name=args['name'], email=args['email'], phone_number=args['phone'])
            db.session.add(user)
            db.session.commit()
        for book in req:
            book = Books.query.get(book)
            assert book, abort(404, message=f"Book with Id <{book}> not found")
            books.append(book)
        currency_id = book.currency_id
        trans = Transaction.create_transaction(customer_id=user.id, currency_id=currency_id, books=books)
        return trans, 201


class TransResult(Resource):
    @marshal_with(transaction_fields)
    def get(self, hash_id):
        trans = Transaction.query.get(hash_id)
        if not trans:
            abort(404, message=f"Transaction with hash <{hash_id}> not found")
        return trans
