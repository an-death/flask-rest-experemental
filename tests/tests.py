import hashlib

import requests

s = requests.Session()

url = f'http://{address}:{port}/'
headers = {'Content-Type': 'application/json'}

# books

books = s.get(url + 'books', headers=headers).json()

assert isinstance(books, list), 'request books returned not list'

cost_to = 500
category = 'business'
business = s.get(''.join((url, 'books', '?', f'category={category}', f'&cost_to={cost_to}')), headers=headers).json()

assert isinstance(business,
                  list), f'request books with filters category={category}, cost_to={cost_to} returned not list'

assert business[-1]['category'] == category, f'response category doesn`t equal to requested'
assert business[0]['cost'] <= 500, f'responce cost does`t equal to requested'

cost_from = 1000
cost_to = 2000
all_expensive = s.get(''.join((url, 'books', '?', f'cost_from={category}', f'&cost_to={cost_to}')),
                      headers=headers).json()

assert isinstance(all_expensive, list), 'request all_expensive returned not list'
assert all_expensive[0] >= cost_from, 'cost from does`t compare with requested.'
assert all_expensive[0] <= cost_to, 'cost to does`t compare with requested.'

# post calculate

data = {
    'name': 'test',
    'email': 'email@email.email',
    'phone': '80000000000',
    'books': ['1', '2', '3']
}
transaction = s.post(''.join((url, 'calculation')), headers=headers, json=data)

assert transaction.status_code == 201, f'Transaction with values {data} does`t created'

transaction = transaction.json()
total_cost = 0
total_id = ''
for book in data['books']:
    result = s.get(''.join((url, 'books', '/', 'r{book}')), headers=headers).json()
    total_cost += result['cost']
    total_id += str(result['id'])

assert transaction[
           'total_cost'] == total_cost, 'Problem with calculation! Total_cost from transaction does`t equal total_cost'
assert transaction['hash_id'] == hashlib.md5(total_id).encode().hexdigest(), 'Hash of transaction is missed!'
