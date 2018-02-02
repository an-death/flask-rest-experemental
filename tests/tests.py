import hashlib

import requests

S = requests.Session()


def __sort_values_by_cost__(list_of_results: list, field: str, index: int):
    if not isinstance(index, int):
        raise ('Index should be Integer. Use "0" for get first index, or "-1" for last')
    if len(list_of_results) == 0:
        raise ValueError('Argument "list_of_results" shouldn`t be empty')
    return sorted(list_of_results, key=lambda result: result[field])[index][field]


def request(url: str, method: str, headers: dict, json=None, retry=1):
    count = 0
    method = method.upper()
    while count <= retry:
        try:
            count += 1
            if method == 'GET':
                S.get(url=url, headers=headers)
            elif method == 'POST':
                if not json:
                    raise ValueError('Arg "json" should be json, not None!')
                S.post(url=url, json=json, headers=headers)
        except Exception as e:
            print(f'Occurred exception {e}. Try:{count}')  # or logging
            continue
    else:
        raise e


class PyTest:
    url = f'http://{address}:{port}/'
    headers = {'Content-Type': 'application/json'}


class PyTestListOfBooks(PyTest):
    category = 'business'
    cost_to = 500
    cost_from = 1000

    @property
    def books(self):
        if hasattr(self, '_books'):
            self.__books = request(self.url + 'books', headers=self.headers, method='get').json()
        return self.__books

    # 1
    def test_1_request_should_return_list_of_books(self):
        assert isinstance(self.books, list), 'request books returned not list'

    # 2
    def test_2_request_should_return_list_of_business_books(self):
        business = S.get(''.join((self.url, 'books', '?', f'category={self.category}')),
                         headers=self.headers).json()
        assert business, 'request returned empty list'
        assert isinstance(business,
                          list), f'request books with filters category={self.category} returned not list'

    # 3
    def test_3_request_should_return_list_of_business_books_with_cost_less_then_500(self):
        business = request(''.join((self.url, 'books', '?', f'category={self.category}', f'&cost_to={self.cost_to}')),
                           headers=self.headers,
                           method='get').json()

        max_cost = __sort_values_by_cost__(business, 'sort', -1)
        assert business, 'request returned empty list'
        assert business[-1]['category'] == self.category, f'response category does`t equal to requested'
        assert max_cost <= self.cost_to, f'response cost does`t equal to requested'

    # 4
    def test_4_request_should_return_expensive_books_with_any_category_with_cost_from_1000(self):
        all_expensive = request(''.join((self.url, 'books', '?', f'cost_from={self.cost_from}')),
                                headers=self.headers,
                                method='get').json()
        min_cost = __sort_values_by_cost__(all_expensive, 'cost', 0)
        assert all_expensive, 'request returned empty list'
        assert isinstance(all_expensive, list), 'request all_expensive returned not list'
        assert min_cost >= self.cost_from, 'cost from does`t compare with requested.'

    # 5
    def test_5_request_should_return_expensive_books_with_any_category_with_cost_less_then_2000(self):
        cost_to = self.cost_to + 1500
        all_expensive = request(''.join((self.url, 'books', '?', f'&cost_to={cost_to}')),
                                headers=self.headers,
                                method='get').json()
        max_cost = __sort_values_by_cost__(all_expensive, 'sort', -1)
        assert all_expensive, 'request returned empty list'
        assert max_cost <= cost_to, 'cost to does`t compare with requested.'

    # 6
    def test_6_request_should_return_expensive_books_with_any_category_between_cost_1000_and_2000(self):
        cost_to = self.cost_to + 1500
        all_expensive = request(
            ''.join((self.url, 'books', '?', f'cost_from={self.cost_from}', f'&cost_to={self.cost_to}')),
            headers=self.headers,
            method='get').json()
        max_cost = __sort_values_by_cost__(all_expensive, 'sort', -1)
        min_cost = __sort_values_by_cost__(all_expensive, 'sort', 0)
        assert all_expensive, 'request returned empty list'
        assert max_cost <= cost_to and min_cost >= min_cost, 'cost to does`t compare with requested.'


# post calculate
class PyTestCalculateTransaction(PyTest):
    default_data = {
        'name': 'test',
        'email': 'email@email.email',
        'phone': '80000000000',
        'books': ['1', '2', '3']
    }

    def create_transaction(self, data):
        return request(''.join((self.url, 'calculation')), headers=self.headers, json=data, method='post')

    def test_7_create_transaction(self):

        assert self.create_transaction(self.default_data). \
                   status_code == 201, f'Transaction with values {self.default_data} does`t created'

    def test_8_wrong_values_for_create_transaction(self):
        pass  # todo check some negative cases!

    def test_9_equivalent_of_calculate_total_cost(self):
        transaction = self.create_transaction(self.default_data).json()
        total_cost = 0
        for book in self.default_data['books']:
            result = request(''.join((self.url, 'books', '/', f'{book}')), headers=self.headers, method='get').json()
            total_cost += result['cost']
        assert transaction['total_cost'] == total_cost, \
            'Problem with calculation! Total_cost from transaction does`t equal total_cost'

    def test_10_check_of_creating_valid_cash_for_data_123(self):
        total_id = ''
        for book in self.default_data['books']:
            result = request(''.join((self.url, 'books', '/', f'{book}')), headers=self.headers, method='get').json()
            total_id += str(result['id'])
        transaction_hash = self.create_transaction(self.default_data).json()['hash_id']
        assert transaction_hash == hashlib.md5(total_id).encode().hexdigest(), 'Hash of transaction is missed!'
