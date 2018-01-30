class Dev:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////test.db'
    SQLALCHEMY_BINDS = {'test': 'sqlite:////test.db'}


class Ops:
    pass  # some production base
