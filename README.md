# Heroku 
The app is hosted here: https://udacityhollywood.herokuapp.com/

# Hollywood APIs 

This readme file describes all needed information for this app, which is hosted on Heroku. 

The Hollywood APIs are used so simplify the process in the crazy Hollywood business. Users can collect Actors and Movies in a database to always find the needed information. 

<!--- Intsallation -->

# Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

# Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

# PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

# Database setup 

Use flask script and flask migrate from the management folder to initialise the data base with the following commands

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

<!--- Running App -->

# Start App

To run the app use: 

python3 app.py



<!--- Endpoints -->

# Existing endpoints

GET '/'
GET '/movies'
POST '/movies'
PATCH '/movies/<movie_id>'
DELETE '/movies/<movie_id>'

GET '/actors'
POST '/actors'
PATCH '/actors/<movie_id>'
DELETE '/actors/<movie_id>'

# Endpoint Discription

All Endpoints need an authentication except the home Endpoint GET '/'


GET '/'
Description:
This is is the home endpoint

Returns:
Json opject that contains 
    {"success": True,
    "message": "Its working!!! At least a bit...",
    "movies": movies}

----
Movies
----

GET '/movies'
Description:
Requests movies from the database

Returns:
Json opject that contains {'succes': True, 'movies': []}
{
  "sucess": true,
  "movies": [
    {
    "id": 1,
    "imdb_rating": 10
    "release_date": "Tue, 19 Jan 2021 00:00:00 GMT",
    "title": "Matrix 4",
    },    {
    "id": 2,
    "imdb_rating": 10,
    "release_date": "Tue, 19 Jan 2021 00:00:00 GMT",
    "title": "Matrix 3",
    }]
}


POST '/movies'
Description:
Posts a new movie into the database

Request:
Json object with { "title": string, "release_date": date, "imdb_rating": int}

Returns:
Json opject that contains {'succes': True, 'message': "Whatever you add, Matrix is the best movie", 'movies': []}
{
  "sucess": true,
  "message": "Whatever you add, Matrix is the best movie"
  "movies": [
    {
   "id": 3,
    "imdb_rating": 10
    "release_date": "Tue, 19 Jan 2021 00:00:00 GMT",
    "title": "Matrix 2",
    }]
}

PATCH '/movies/<movie_id>'
Description:
Patches a movie from the database

Request:
movie_id in URL 
Json object with { "title": string, "release_date": date, "imdb_rating": int}

Returns:
Json opject that contains {'succes': True, 'movies': []}
{
  "sucess": true,
  "movies": [
    {
    "id": 1,
    "imdb_rating": 10
    "release_date": "Tue, 19 Jan 2021 00:00:00 GMT",
    "title": "Matrix 4",
    }]
}


DELETE '/movies/<movie_id>'
Description:
Deletes a specific movie from the DB by its id. 
Dont delete any Matrix movie... I mean you can and it wont have any other impacts...
But no one should delete a Matrix movie... masterpiece

Request:
movie_id in URL 

Returns:
Json opject that contains {'succes': True, "delete": int, 'deleted_movie': []}
{
  "sucess": true,
  "delete": 1
  "movies": [
    {
    "id": 1,
    "imdb_rating": 10
    "release_date": "Tue, 19 Jan 2021 00:00:00 GMT",
    "title": "Matrix 4",
    }]
}

---
Actors
---

GET '/actors'
Description:
Requests actors from the database

Returns:
Json opject that contains {'succes': True, 'actors': []}
{
    "sucess": true,
    "actors": [
        {
        "id": 1,
        "name": "Keanu Reeves",
        "age": 56,
        "gender": "Male",
        },  {
        "id": 2,
        "name": "Carrie-Anne Moss",
        "age": 53,
        "gender": "Female",
        }]
}



POST '/actors'
Description:
Posts a new actor into the database

Request:
Json object with { "name": string, "age": int, "gender": string}

Returns:
Json opject that contains {'succes': True, 'actors': []}
{
  "sucess": true,
  "actors": [
        {
        "id": 1,
        "name": "Keanu Reeves",
        "age": 56,
        "gender": "Male",
        }]
}

PATCH '/actors/<movie_id>'
Description:
Patches an actor from the database

Request:
actor_id in URL 
Json object with { "name": string, "age": int, "gender": string}

Returns:
Json opject that contains {'succes': True, 'movies': []}
{
  "sucess": true,
  "actors": [
        {
        "id": 1,
        "name": "Keanu Reeves",
        "age": 56,
        "gender": "Male",
        }]
}


DELETE '/actors/<actor_id>'
Description:
Deletes a specific actor from the DB by its id. 

Request:
actor_id in URL 

Returns:
Json opject that contains {'succes': True, 'deleted_actor': []}
{
    "sucess": true,
    "deleted_actor": [
        {
        "id": 1,
        "name": "Keanu Reeves",
        "age": 56,
        "gender": "Male",
        }]
}


<!--- Testing -->

# Test Endpoints

test_app has a test for every endpoint. Each endpoint is tested, if it works with the correct rights and makes sure it doesnt work with the wrong permissions
To run tests use 

python3 test_app.py


<!--- Rolles & Rights -->

Roles and Rights are managed with Auth0. 

# Roles
There are three roles

Casting Assistant
    Can view actors and movies

Casting Director
    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies

Executive Producer
    All permissions a Casting Director has and…
    Add or delete a movie from the databas
