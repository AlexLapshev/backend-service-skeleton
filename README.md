## Installation

Create virtual environment

`virtualenv venv`

Activate it

`source venv/bin/activate`

Install required packages

`pip install -r requirements/base.txt`

Run a database from a docker-compose file

```
cd etc
docker-compose up -d
```

Apply migrations 

```
cd ..
alembic upgrade head
```

To run the app 

`python main.py`

## Examples of CURL requests

Create user

```
curl --location --request POST '127.0.0.1:8000/v1/user' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Fake Name"
}'
```

Get user

```
curl --location --request GET '127.0.0.1:8000/v1/user/34' \
--header 'accept: application/json' \
--header 'Content-Type: application/json'
```

Add transaction

```
curl --location --request POST '127.0.0.1:8000/v1/transaction' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": {user_id},
    "amount": "100.00",
    "type": "DEPOSIT",
    "timestamp": null,
    "uid": null
}'
```

```
curl --location --request POST '127.0.0.1:8000/v1/transaction' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": {user_id},
    "amount": "100.00",
    "type": "DEPOSIT",
    "timestamp": "2023-03-05T00:26:53.079192",
    "uid": "fb850ab6-daf8-48cb-8304-8c45daf13cb6"
}'
```

Get transaction

```
curl --location --request GET '127.0.0.1:8000/v1/transaction/fb850ab6-daf8-48cb-8304-8c45daf13cb6' \
--header 'accept: application/json' \
--header 'Content-Type: application/json'
```

Get user with date filtering

```
curl --location --request GET 'http://localhost:8000/v1/user/{user_id}?date=2023-01-30T00:00:00' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw ''
```

## Tests

To run tests while the app is running 

`pytest tests`
