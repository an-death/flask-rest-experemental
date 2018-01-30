import hashlib
from datetime import datetime
from os import urandom

from sqlalchemy.orm import validates

from app import db


class Meta(db.Model):
    __abstract__ = True
    __tablename__ = None
    def __repr__(self):
        return ('<{}({})>'.format(self.__tablename__, ', '.join(
            _ + ': ' + str(atr) for _, atr in self.__dict__.items() if not _.startswith('_'))))


books_transactions = db.Table('association_books_transactions', Meta.metadata,
                              db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.transaction_hash')),
                              db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
                              )


class Customer(Meta):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    phone_number = db.Column(db.String)  # todo upgrade validation on sa_utils

    transactions = db.relationship('Transaction', backref=db.backref('customer'))

    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number

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

    transaction_hash = db.Column(db.Text, unique=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    date = db.Column(db.DateTime)
    hash_id = db.synonym('transaction_hash')

    books = db.relationship('Books', secondary=books_transactions, back_populates='transactions')

    def __init__(self, transaction_hash, customer_id, books: list):
        self.transaction_hash = transaction_hash
        self.customer_id = customer_id
        self.date = datetime.now()
        for book in books:
            assert isinstance(book, Books)
            self.books.append(book)

    @property
    def total_cost(self):
        return sum((float(book.cost) for book in self.books))

    @classmethod
    def create_transaction(cls, customer_id, books: list):
        transaction_hash = hashlib.md5((''.join(str(b.id) for b in books)).encode()).hexdigest()
        trans = cls.query.get(transaction_hash)
        if not trans:
            trans = cls(transaction_hash, customer_id, books)
            db.session.add(trans)
            db.session.commit()
        return trans


class Category(Meta):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)

    books = db.relationship('Books', backref=db.backref('category_desc'))

    def __init__(self, name):
        self.name = name


class Books(Meta):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ISBN = db.Column(db.String(13), unique=True)  # todo add validation
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    cost = db.Column(db.Float)  # todo upgrade filed to sqla_utils.types.currency
    description = db.Column(db.Text(300), default=urandom(200))

    transactions = db.relationship('Transaction', secondary=books_transactions, back_populates='books')

    def __init__(self, ISBN, category_id, cost, description=None):
        self.ISBN = ISBN
        self.category_id = category_id
        self.cost = cost
        self.description = description

    @property
    def category(self):
        return self.category_desc.name

    @classmethod
    def add_book(cls, ISBN, category, cost):
        category = Category.query.filter(Category.name == category).first_or_404()
        book = cls(ISBN, category.id, cost)
        db.session.add(book)
        db.session.commit()
        # return book.get()


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from database import Dev

    engine = create_engine(Dev.SQLALCHEMY_DATABASE_URI)
    db.metadata.bind = engine
    db.drop_all(engine)
    db.create_all(engine)
    book = Books(ISBN='01-0101-0111', category_id=1, cost=500)
    horrors = Category(name='horrors')
    business = Category(name='business')
    book2 = Books(ISBN='01-0101-0110', category_id=2, cost=200.2)
    db.session.add_all([horrors, business, book, book2])
    db.session.commit()
