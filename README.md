# Job Portal API Backend

## Description

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

The backend is designed to work for three types of users:
* Casting Assistant:

    Can view actors and movies
* Casting Director:

    * All permissions a Casting Assistant has and…
    * Add or delete an actor from the database
    * Modify actors or movies
* Executive Producer:
    * All permissions a Casting Director has and…
    * Add or delete a movie from the database

Authorization of users is enabled via Auth0 in which three seperate roles (assistant, director and productor) have been created and assigned seperate permissions.
### Installing Dependencies
#### Python 3.12

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.
##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Database setup
The `models.py` file contains connection instructions to the Postgres database, which must also be setup and running. Provide a valid username and password, if applicable.

1. Create a database with name `app` using Psql CLI:

```
create database app;
```

2. Initiate and migrate the database with the following commands in command line:

```
flask db init
flask db migrate
flask db upgrade
```

This will create all necessary tables and relationships to work with the project.

## Data Modelling

The data model of the project is provided in `models.py` file in the root folder. The following schema for the database and helper methods are used for API behaviour:

- There are 3 tables created: Actors, Movies, and Assistant.
## Running the local development server
To run the API server on a local development environmental the following commands must be additionally executed:

### On Linux: export
```
export FLASK_APP=wgsi.py
export FLASK_ENV=development
```

### On Windows: set
```
set FLASK_APP=wgsi.py
set FLASK_ENV=development
```

### API Server

All accessable endpoints of the project are located in the `app.py` file.

Run the following command in the project root folder to start the local development server:

```
flask run
```

## RBAC credentials and roles

Auth0 was set up to manage role-based access control for two users. The API documentation below describes, among others, by which user the endpoints can be accessed. Access credentials and permissions are handled with JWT tockens which must be included in the request header.

### Permissions

Actors can access API endpoints that have the following permission requirements:
`'read:actors'` - Get a list of actors
`'create:actors'` - Create new actor
`'update:actors'` - Update actor by id
`'delete:actors'` - Delete actor by id


Movies can access API endpoints that have the following permission requirements:

`'read:movies'` - Get a list of movies
`'create:movies'` - Create new movie
`'update:movies'` - Update movie by id
`'delete:movies'` - Delete movie by id

There are also publicly available endpoints that do not require authorization. This is done to ensure every user can see the general information about jobs and candidates.

##### Postman
We recommend to use Postman Application to call api endpoint [here](api.postman_collection.json)
![image](docs/img.png)
We have 3 tokens corresponding to 3 roles valid `until 12 a.m on Sunday December 2024`


## API endpoints

### Public endpoints
#### POST '/login'
-  Get Auth0 token permission to fetch other API
- Request Arguments: object contains 2 key: `email` and `password`
- Return: A JSON object contains access_token

Sample curl request:
`curl -X GET http://127.0.0.1:5000/login -d '{ "email":"assistant@gmail.com", "password": "123456789abc@" }'`

Sample response:
```
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjVxcHBDaDlzaC1NYURNMnVObmhYQyJ9.eyJpc3MiOiJodHRwczovL2Rldi1td29od2UxN3A4anRocXVhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzUxNzAxNmFkMjA5MTE4YzRiNDMyYzIiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAvYXBpIiwiaWF0IjoxNzMzNTYwNDk0LCJleHAiOjE3MzM2NDY4OTQsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiMWNvaWhIdjEwdmNPUkhRRUpJWFVwcGxwVGxqSW01N3MiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9yIiwicmVhZDptb3ZpZSJdfQ.UqZfiePwZoXaMBNb9HYZ4sUE-7jnteMUyywXgW02Z0aTdrdQnHzoPmDxig6dfodXkPGerTl-5md1BcUZJHqYZ4PaM9Xo5yaBvqmhdzPiO-thUFyhDkxejLwlMgv96px1Pv-1NhZgm5gSgbmsk-IdSeFcsNG04fxjB_4NrH8wEPpzLP0swjaZRaEZlg6yvhSboltcAEmpN4mBCqPVe8kZIqPsApVvzBnWSpJaYsmUIiAHD1hx7DNS7ecmEXR8FZoGTiOgbcwbbgfFGWoWKgAUmf5py6mUDSOJnkc3DoWHMNxRpZCsxi6id0FKAIhOIud5dL6qe5d7PWxjtN8o6l2trg",
    "expires_in": 86400,
    "token_type": "Bearer"
}
```

#### GET '/actors'
- Fetches a dictionary with id and names of actors who posted their information to the database.
- Request Arguments: None
- Returns: A list of actors

Sample curl request:
`curl -X GET http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY"`

Sample response:
```
[{
    "age": 20,
    "gender": "male",
    "id": "01JEG142WBHHXFKDJ30HR7T1DV",
    "name": "Google"
}]
```
#### GET '/actors/<string:id>'
- Fetches detail information about a actor by ID
- Request arguments: None
- Returns: A JSON dictionary with all actors infomration.

Samples curl request:

`curl -X GET http://127.0.0.1:5000/actors/01JEG1P2VFRD46V7BDAEJZF771 -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY"`

Sample response:
```
{
   "age": 20,
   "gender": "male",
   "id": "01JEG1P2VFRD46V7BDAEJZF771",
   "movies": [],
   "name": "name"
}
```


#### GET '/movies'
- Fetches short information about all movies
- Request argument: none
- Returns: A JSON object - list of dictionaries with the main information about movies

Sample curl request:

`curl -X GET http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY"`

Sample response:
```
[{
  "id": "01JEG1XWHDKCEW7J74P4TTSMS4",
   "release_date": "2025-01-06",
    "title": "the movie title"
}]
```

#### GET '/movies/<string:id>'
- Fetches movies information about a particular movie by id
- Request arguments: none
- Returns: a JSON object - a dictionary with all information about a movie

Sample curl request:

`curl -X GET http://127.0.0.1:5000/movies/01JEG24WV4YYRTX9G8YX45J1RR -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY"`

Sample response:
```
{
  "actors": [],
   "id": "01JEG24WV4YYRTX9G8YX45J1RR",
   "release_date": "2025-01-06",
   "title": "The legend of the sun"
}
```


#### POST '/actors'
- Creates a actor in the database
Sample curl request:
```
curl -d '{"name":"Google", "age": 20, "gender": "male"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY" -X POST http://127.0.0.1:5000/actors
```

Sample response:
```
{
   "age": 20,
   "gender": "male",
   "id": "01JEG1P2VFRD46V7BDAEJZF771",
   "name": "Google"
}

```

#### POST '/movies'
- Creates a movies in the database
  Sample curl request:
```
curl -d '{"title":"The legend of the sun"}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY" -X POST http://127.0.0.1:5000/movies
```

Sample response:
```
{
   "id": "01JEG2BZZPY9EY16H0SKNWKAP1",
   "release_date": "2025-01-06",
   "title": "The legend of the sun"
}
```

#### PATCH '/actors/<string:id>'
- Enables updating of existing actor data in the database or add new actor information
- Request arguments: a JSON formatted object.
- Returns: a JSON object

Samples curl request:
```
curl -d '{ "name": "Amazon Cloudformation "}' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY" -X POST http://127.0.0.1:5000/actors/01JEG2BZZPY9EY16H0SKNWKAP1
```
Sample response:
```
{
  "age": 20,
  "gender": "male",
  "id": "01JEG2WPJTQKC89Z3F55W8MMQV",
  "name": "Amazon Cloudformation"
}
```

#### PATCH '/movies/<string:id>'
- Enables updating of existing movie data in the database or add new movie information
- Request arguments: a JSON formatted object.
- Returns: a JSON object

Samples curl request:
```
curl -d '{ "title": "Amazon Cloudformation" }' -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN_COMPANY" -X POST http://127.0.0.1:5000/movies/01JEG2BZZPY9EY16H0SKNWKAP1
```
Sample response:
```
{
   "id": "01JEG2BZZPY9EY16H0SKNWKAP1",
   "release_date": "2025-01-06",
   "title": "Amazon Cloudformation"
}
```

#### DELETE '/actors/<string:id>'
- Deletes all actor by id information from the database
- Request parameters: none
- Returns: a JSON object with success status true and company id when the company information was successfully deleted from the database.

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/actors/01JEG2BZZPY9EY16H0SKNWKAP1 -H "Authorization: Bearer $USER_TOKEN_COMPANY"
```

Sample response:
```
{}
```

#### DELETE '/movies/<string:id>'
- Deletes all actor by id information from the database
- Request parameters: none
- Returns: a JSON object with success status true and movie id when the company information was successfully deleted from the database.

Sample curl request:
```
curl -X DELETE http://127.0.0.1:5000/movies/01JEG2BZZPY9EY16H0SKNWKAP1 -H "Authorization: Bearer $USER_TOKEN_COMPANY"
```

Sample response:
```
{}
```

#### POST '/movies/<string:movie_id>/actors/<string:actor_id>'
- Add actor into movie
- Request arguments: None
- Returns: a JSON object

Sample curl request:
```
curl -X POST http://127.0.0.1:5000/movies/01JEG3E5PHXZ53M8P6SXX5PJSQ/actors/01JEG3E5MBZJJ1MRWQAGTQ5E5G -H "Authorization: Bearer $USER_TOKEN_COMPANY"
```

Sample response:
```
{
  "actors": [{
     "age": 20,
     "gender": "male",
     "id": "01JEG3E5MBZJJ1MRWQAGTQ5E5G",
     "name": "name"
  }],
   "id": "01JEG3E5PHXZ53M8P6SXX5PJSQ",
   "release_date": "2025-01-06",
   "title": "The legend of the sun"
}

```

## Testing

The testing of all endpoints was implemented with unittest. Each endpoint can be tested with one success test case and one error test case. RBAC feature can also be tested for company user and candidate user.

All test cases are soted in `test_api.py` file in the project rool folder.

Before running the test application, create `testdb` database using Psql CLI:
```
create database testdb
```

Then in the command line interface run the test file:

`python3 test_api.py`

## Heroku Deployment and Base URL

The backend application has been deployed on Heroku and can be accessed live at
```
https://casting-agency-specifications-97639fdbf19d.herokuapp.com/
```