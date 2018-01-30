from os import urandom

from sqlalchemy.orm import validates
from sqlalchemy_utils.types import CurrencyType  # , PhoneNumber

from app import db


class Meta(db.Model):
    __abstract__ = True
    __tablename__ = None

    def __repr__(self):
        return ('<{}({})>'.format(self.__tablename__, ', '.join(
            _ + ': ' + str(atr) for _, atr in self.__dict__.items() if not _.startswith('_'))))


books_transactions = db.Table('association_books_transactions', Meta.metadata,
                              db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
                              db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
                              )


class Customer(Meta):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone_number = db.Column(db.String)  # todo upgrade validation on sa_utils

    transactions = db.relationship('Transaction', backref=db.backref('customer'))

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        assert number.startswith('8') or number.startswith('+7')
        if number.startswith('+'):
            assert number[1:].isdigit()
        return number


class Transaction(Meta):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_hash = db.Column(db.Text, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    date = db.Column(db.DateTime)
    purchase_cost = db.Column(CurrencyType)
    books = db.relationship('Books', secondary=books_transactions, back_populates='transactions')


class Category(Meta):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)

    books = db.relationship('Books', backref=db.backref('category'))


class Books(Meta):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ISBN = db.Column(db.String(13), unique=True)  # todo add validation
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    cost = db.Column(CurrencyType)  # todo upgrade filed to sqla_utils.types.currency
    description = db.Column(db.Text(300), default=urandom(200))

    transactions = db.relationship('Transaction', secondary=books_transactions, back_populates='books')
