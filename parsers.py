from flask_restful import reqparse

default_help_string = 'Required field <{}> cannot be empty'
def get_parsers():
    parsers = {
        'book_parser': reqparse.RequestParser(),
        'calculate_parser': reqparse.RequestParser()
    }

    parsers['calculate_parser'].add_argument('name', type=str, required=True, help=default_help_string.format('name'))
    parsers['calculate_parser'].add_argument('email', type=str, required=True, help=default_help_string.format('email'))
    parsers['calculate_parser'].add_argument('phone', type=str, required=True, help=default_help_string.format('phone'))
    parsers['calculate_parser'].add_argument('books', type=list, required=True,
                                             help=default_help_string.format('books'))

    parsers['book_parser'].add_argument('category', type=str)
    parsers['book_parser'].add_argument('cost', type=float)
    parsers['book_parser'].add_argument('cost_from', type=float)
    parsers['book_parser'].add_argument('cost_to', type=float)

    return parsers['book_parser'], parsers['calculate_parser']
