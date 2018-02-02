from flask_restful import reqparse

default_help_string = 'Required field <{}> cannot be empty'
def get_parsers():
    parsers = dict(
        book_parser=reqparse.RequestParser(),
        calculate_parser=reqparse.RequestParser(),
        book_creater=reqparse.RequestParser()
    )
    parsers['calculate_parser'].add_argument('name', type=str, required=True, help=default_help_string.format('name'))
    parsers['calculate_parser'].add_argument('email', type=str, required=True, help=default_help_string.format('email'))
    parsers['calculate_parser'].add_argument('phone', type=str, required=True, help=default_help_string.format('phone'))
    parsers['calculate_parser'].add_argument('books', type=list, required=True,  # todo bug - doesnt type=list work
                                             help=default_help_string.format('books'))

    parsers['book_parser'].add_argument('category', type=str)
    parsers['book_parser'].add_argument('ISBN', type=str)
    parsers['book_parser'].add_argument('cost', type=float)
    parsers['book_parser'].add_argument('cost_from', type=float)
    parsers['book_parser'].add_argument('cost_to', type=float)

    parsers['book_creater'].add_argument('category', type=str, required=True)
    parsers['book_creater'].add_argument('ISBN', type=str, required=True)
    parsers['book_creater'].add_argument('cost', type=float, required=True)
    parsers['book_creater'].add_argument('currency_id', type=int, required=True)


    return parsers['book_parser'], parsers['calculate_parser'], parsers['book_creater']
