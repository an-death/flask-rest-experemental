from flask_restful import reqparse


def get_parsers():
    parsers = {
        'book_parser': reqparse.RequestParser(),
        'calculate_parser': reqparse.RequestParser()
    }

    parsers['calculate_parser'].add_argument('name', type=str, help='name cannot be empty')
    parsers['calculate_parser'].add_argument('email', type=str, help='email cannot be empty')
    parsers['calculate_parser'].add_argument('phone', type=str, help='phone cannot be empty')
    parsers['calculate_parser'].add_argument('books', type=list, help='books cannot be empty')

    parsers['book_parser'].add_argument('category', type=str)
    parsers['book_parser'].add_argument('cost', type=float)
    parsers['book_parser'].add_argument('cost_from', type=float)
    parsers['book_parser'].add_argument('cost_to', type=float)

    return parsers['book_parser'], parsers['calculate_parser']
