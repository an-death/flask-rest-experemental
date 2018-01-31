# flask-rest-experemental
trying to write rest-api om flask


books:

`curl -X GET http://url/books`
parameters:
    [category, cost, cost_from, cost_to]

add book:

`curl -X POST http://url/books 
  -H 'content-type: application/json' \
  -d '{"ISBN": "Python", "category":"For Coders", "cost":"500"}'`
  
del word: 

`curl -X DELETE http://example.com/api/words/{id} -H 'authorization: Token $TOKEN'` 


vacancies:

`curl -X GET http://127.0.0.1:5000/api/words/{id}/vacancies/ -H 'authorization: Token $TOKEN'`

parameters: 
    [date__gte, date__lte, date__gt, date__lt, page] 
    
    date_format must be : "YYYY-MM-DD"
    
For start celery background task use:

`celery -A django_rest worker -l DEBUG --pool=solo -B &`