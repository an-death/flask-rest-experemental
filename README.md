# flask-rest-experemental
trying to write rest-api om flask with python 3.6


books:

`curl -X GET http://url/books`

parameters:
    [category, cost, cost_from, cost_to]

add book:

`curl -X POST http://url/books 
  -H 'content-type: application/json' \
  -d '{"ISBN": "Python", "category":"For Coders", "cost":"500"}'`
  parameters:
  [ISBN, category, cost]


calculate:

`curl -X POST http://url/calculate`

parameters: 
    [name, email, phone, books:list] 
    
transaction:

`curl -X POST http://url/transsaction/<hash>`

hash = transaction 