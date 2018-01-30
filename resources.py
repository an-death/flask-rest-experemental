from flask_restful import Resource, fields, marshal_with, abort

from app import db
from models.models import Customer, Transaction, Books
from parsers import get_parsers

book_fields = {
    'ISBN': fields.String,
    'category': fields.String,
    'cost': fields.Float
}

calculate_fields = {
    'books': fields.List,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String(attribute='phone_number')
}
transaction_fileds = {
    'transaction': fields.String,
    'uri': fields.Url('transaction', endpoint='transaction', absolute=True, scheme='http')
}

book_parser, calculate_parser = get_parsers()


class BookDescription(Resource):
    @marshal_with(book_fields)
    def get(self, ISBN):
        book = Books.query.fiter(ISBN=ISBN).first_or_404()
        if not book:
            abort(404, message="Book with ISBN {} not found".format(ISBN))
        return book

    @marshal_with(book_fields)
    def put(self, ISBN):
        pass  # todo add if needed

    def delete(self, ISBN):
        pass  # todo add if needed


class BooksList(Resource):
    @marshal_with(book_fields)
    def get(self):
        args = book_parser.parse_args()
        query = Books.query
        if args['category']:
            query = query.filter(category=args['category'])
        if args['cost_from']:
            query = query.filter(Books.cost >= args['cost_from'])
        if args['cost_to']:
            query = query.filter(Books.cost <= args['cost_to'])
        if args['cost']:
            query = query.filter(cost=args['cost'])
        return query.all()

    def post(self):
        pass  # todo add when its need


class Calculate(Resource):
    # todo add calculation get and put method's for customize
    def post(self):
        args = calculate_parser.parse_args()
        user = Customer.query.filter(Customer.email == args['email']).one()
        if not user:
            user = Customer(name=args['name'], email=args['email'], phone_number=args['phone'])
            db.session.add(user)
            db.session.commit()
        trans = Transaction.create_transaction(customer_id=user.id, books=args['books'])
        db.session.add(trans)
        db.session.commit(trans)
        return trans, 201


class TransResult(Resource):
    @marshal_with(transaction_fileds)
    def get(self, hash):
        return Transaction.get_or_404(hash)
