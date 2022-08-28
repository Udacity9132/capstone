
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. There are two roles in the company: Casting Assistant and Casting Director. They have different permissions to view, add, update and delete actors and movies. The application is secured by Auth0 and deployed on Heroku. 

Heroku URL: https://capstone-uda.herokuapp.com/

# Tech Stack

Database: Postgres

Server language and framework: Python and Flask

Authentication service: Auth0

Deployment: Heroku

# Getting started

1. Initialize a virtualenv and activate it
$ python3 -m venv env 
$ source env/bin/activate

2. Install the dependencies
$ pip3 install -r requirements.txt

3. Run source setup.sh to set the JWTs and auth0 credentials and set up the Database

$ python3 manage.py db upgrade

$ python3 manage.py seed

$ source setup.sh

5. Run the development server

python3 app.py or

$ export FLASK_APP=myapp

$ export FLASK_ENV=development

flask run

# Testing

$ python3 manage.py db downgrade

$ python3 manage.py db upgrade

$ python3 manage.py seed


# Roles:

Casting Assistant
- Can view actors and movies

Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
- Add or delete movies from the database

# Models

Movies with attributes title and release date
Actors with attributes name, age and gender

## API Reference

# Endpoints

GET '/movies'
- Returns all movies in database
- Authorised roles: Casting Assistant and Casting Director
- Example: curl http://127.0.0.1:5000/movies

{
  "movies":
  [{
    "title": example movie,
    "release_date": "2022-01-01",
    "id": 1,
  },
    "title": london movie,
    "release_date": "2022-03-03",
    "id": 2,
  }],
    "success": true
}

GET '/actors'
- Returns all actors in database
- Authorised roles: Casting Assistant and Casting Director
- Example: curl http://127.0.0.1:5000/actors

{
  "actors":
  [{
    "age": 25,
    "gender": "male",
    "id": 1,
    "name": “Michael Young”
  },
  "age": 50,
  "gender": female
  "name": Louise M
  }],
    "success": true
}

GET '/movies/<int:id>'
- Returns a single movie by id
- Authorised roles: Casting Assistant and Casting Director
- Example: curl http://127.0.0.1:5000/movies/1

{
  "movie":
  {
    "title": example movie,
    "release_date": "2022-01-01",
    "id": 1,
  },
    "success": true
}

GET '/actors/<int:id>'
- Returns a single actor by id
- Authorised roles: Casting Assistant and Casting Director
- Example: curl http://127.0.0.1:5000/actors/1

{
  "actor":
  {
    "age": 25,
    "gender": "male",
    "id": 1,
    "name": “Michael Young”
  },
    "success": true
}

POST '/movies'
- adds a new movie to the database
- Authorised roles: Casting Director
- Example: curl http://127.0.0.1:5000/movies -X POST - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"title": "example movie", "release_date": "2022-01-01"}'

{
  "movies":
  {
    "title": "example movie",
    "release_date": "2022-01-01",
    "id": 4,
  },
  "success": true
}


POST '/actors'
- adds a new actor to the database
- Authorised roles: Casting Director
- Example: curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{ "name": "Michael", "age": 25, "gender": "male" }'

{
  "actor":
  {
    "age": 25,
    "gender": "male",
    "id": 4,
    "name": “Michael”
  },
  "success": true
}

PATCH '/movies/int:id'
- Update data of a movie
- Authorised roles: Casting Director
- Example: curl http://127.0.0.1:5000/movies -X PATCH - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"title": "example movie", "release_date": "2022-01-01"}'

{
  "movies":
  {
    "title": "example movie",
    "release_date": "2022-01-01",
    "id": 4,
  },
  "success": true
}

PATCH '/actors/int:id'
- Update data of an actor
- Authorised roles: Casting Director
- Example: curl http://127.0.0.1:5000/actors -X PATCH -H "Content-Type: application/json" -d '{ "name": "Michael", "age": 25, "gender": "male" }'

{
  "actor":
  {
    "age": 25,
    "gender": "male",
    "id": 4,
    "name": “Michael”
  },
  "success": true
}

DELETE '/movies/int:id'
- Delete a movie from the database 
- Authorised roles: Casting Director
- Example: curl http://127.0.0.1:5000/movies/1 -X DELETE 

{
    "message": "Movie deleted"
    "success": true
}

DELETE '/actors/int:id'
- Delete an actor from the database
- Authorised roles: Casting Director
- Example: curl http://127.0.0.1:5000/actor/1 -X DELETE 

{
    "message": "Actor deleted"
    "success": true
}

# Error handlers 

Errors are returned as JSON: 
{
    'success': False,
    'error': 400,
    'message': 'Bad request'
}

# Error types
- 400: Bad request
- 404: Not found
- 403: Forbidden
- 422: Unprocessable
- 500: Internal Server Error