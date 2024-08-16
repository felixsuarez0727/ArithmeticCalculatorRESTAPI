# FastAPI Arithmetic Calculator RestAPI

This is a RestAPI developed on Python and FastApi to provide endpoints with operations like: 

- addition
- subtraction
- multiplication
- division 
- square root
- random string generation

To provide persistance of the operations the Backend saves the data in a SQLite database named: `db.db`

For Random String Generation it consumes a web service provided by Random.Org

## Security
Security is ensured using JWT tokens generated during user authentication, with credentials securely stored in the backend database's `User` table. The user employes the 'login' endpoint with username and password.

## Configuration

The FastAPI uses an `.env` file for environment-specific settings: 

````bash
API_KEY_RANDOM="b5544438-3078-4ef2-af6d-30b7550d7049"
SECRET_KEY="DEVELOPER"
EXPIRATION_TIME=3600
FRONTEND_ORIGIN = "http://localhost:5173"
````

- API_KEY_RANDOM: It is used to set the apikey from the random.org service.
- SECRET_KEY: It it the secret word use for creating the JWT tokens.
- EXPIRATION_TIME= This is an integer used to set the number of minutes a token is valid.
- FRONTEND_ORIGIN= This must be set to specifically allow connections from the Hosting where its located the `React Arithmetic Calculator WebApp`.

## Endpoint Descriptions: 
The API has the version 1.

### Login
URL: ``/v1/login``

This endpoint with HTTP Method POST is used to authenticate the user, this delivers a JWT Token user to authenticate the incoming requests.
The username available in database is: `dev` and password: `1234`

Body:
```
{
  "username": "string",
  "password": "string"
}
```
Token Response:
```
{
  "access_token": "string",
  "token_type": "string"
}
```
Error Response:
```
{
  "detail": "string"
}
```
### Logout
URL: ``/v1/logout``

This endpoint with HTTP Method POST is used to LogOut the user. This endpoint revokes the token.
The request must have the header ``Authorization`` to receive the token that is going to revoked.

### Validate Token
URL: ``/v1/validate_token``

This endpoint with HTTP Method POST is used to validate the token to restringe the access in private modules of the FrontEnd. If the token is invalid or expired, you need to logout (if necessary) and login.
The request must have the header ``Authorization`` to receive the token.

### Random String
URL: ``/v1/random_string``

This endpoint with HTTP Method GET is used to generate a Random String, this endpoint internally consumes a Webservice provided by Random.Org
The request must have the header ``Authorization`` to allow the endpoint usage.

### Common Arithmetic Operations: addition, subtraction, multiplication & division
- URL: ``/v1/addition``
- URL: ``/v1/subtraction``
- URL: ``/v1/multiplication``
- URL: ``/v1/division``

This endpoints with HTTP Method POST are use to perform basic Arithmetic Operations. 
The request must have the header ``Authorization`` to allow the endpoint usage.

Body:
```
{
  "num_a": float,
  "num_b": float,
  "operation": "addition|subtraction|multiplication|division"
}
```
Successful Response:
```
{
  "data": 0
}
```
Error Response:
```
{
  "detail": "string"
}
```

### Square Root
- URL: ``/v1/square_root``

This endpoints with HTTP Method POST calculates the square root of a number.
This endpoint validates negative numbers and zero input. 
The request must have the header ``Authorization`` to allow the endpoint usage.

Body:
```
{
  "number": float,
}
```
Successful Response:
```
{
  "data": 0
}
```
Error Response:
```
{
  "detail": "string"
}
```

### Record
- URL: ``/v1/record``

This endpoint with HTTP Method GET show all the data of operation records that a user has perform in the App.
The request must have the header ``Authorization`` to allow the endpoint usage.

URL: http://127.0.0.1:8000/v1/record/?page=1&per_page=10&sort_by=id&sort_order=asc&search=
```
page: Number of Page
per_page: Items per page
sort_by: id | amount | type
sort_order:  desc | asc
search: Word or number to search
```
Successful Response:
```
[
  {
    "id": 0,
    "operation_id": 0,
    "user_id": 0,
    "amount": "string",
    "user_balance": 0,
    "operation_response": "string",
    "date": "string",
    "deleted_at": "string",
    "type": "string"
  }
]
```
Error Response:
```
{
  "detail": "string"
}
```

### Record
- URL: ``/v1/record{id}``

This endpoint with HTTP Method DELETE will perform a ``Soft Delete`` of the ``{id}``. This means it will delete a record operation. 
The request must have the header ``Authorization`` to allow the endpoint usage.

Successful Response:
```
{
  "data": "string"
}
```
Error Response:
```
{
  "detail": "string"
}
```
## Installation & Running the API
1. Install Python and PIP in your machine.

2. Ensure you have the Python environment working properly.

3. Open a Terminal and install libraries: 
```
pip install "fastapi[standard]"

pip python-jose 

pip install python-dotenv

pip install pydantic

```
4. For Running in development mode: ``fastapi dev acra.py``
5. For Running in Production mode: ``fastapi run acra.py`` This will launch the app in the localhost: ``http://localhost:8000/docs``

## LIVE VERSION
Find the running app here:

- BackEnd: https://img-arithmetic-calculator-restapi-3rzadn5oaa-uc.a.run.app/docs
- FrontEnd: https://main--react-arithmetic-calculator-2024.netlify.app/

