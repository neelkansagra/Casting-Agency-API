# FSND Capstone project

## Content

1. [Motivation](#Motivation)
2. [Getting Started](#Start-locally)
3. [Data Modeling](#data-modeling)
4. [API Documentation](#API)
5. [Authentication](#Authentication)

<a name="Motivation"></a>
## Motivation
This project is the final project for Udacity's Full Stack Developer Nanodegree. This project aims at facilitating a Casting agency from their process of creating movies and managing and assigning actors to those movies by creating an API.It covers the following technical topics:

1. Database modeling with postgres & sqlalchemy (models.py)
2. API to perform CRUD application on actors and movies. (api.py)
3. Automatic testing of endpoints by unittest. (test_app.py and test_role_based_app.py)
4. Authentication and role based access control. (auth.py)
5. Deployment to heroku.

<a name="Start-locally"></a>
## Getting Started

First download this repository in your local machine and open command prompt. 'cd' into folder where you've downloaded this repository.
Make sure you have downloaded [python3](https://www.python.org/downloads/) ,pip and [postgreSQL](https://www.postgresql.org/download/)
in your local machine.

To start and run development server,
1. Initialize and activate virtualenv
```bash
$ virtualenv --no-site-packages env
$ source env/scripts/activate
```
2. Download and install dependencies
```bash
$ pip3 install -r requirements.txt
```
3. Change the database configuration of your postgreSQL database in config.py according to the configuration on your local machine.
```python
database = {
        "database_name": "casting",  # name of your database (run createdb casting to create a new database)  
        "username":"postgres",       # username of your database admin (default is postgres)
        "username_password":"abcd",  # password of your user 
        "port":"localhost:5432"      # default port of your database
}
```
4. Running the development server
```bash
$ python api.py
```
5. (optional) Running tests.

    Delete the old casting database and create a new casting database. 
```bash
$ sudo su postgres   // Switch user to your postgres admin
$ dropdb casting
$ createdb casting
$ exit
```
Note: This step is to have a fresh database for running test since endpoints in test_app are depended on column ids.

Running test locally
```bash
$ python3 test_app.py
$ python3 test_role_based_app.py
```
You should get something like this upon successfull execution.
```bash
$ python test_app.py
.....................
----------------------------------------------------------------------
Ran 21 tests in 28.132s

OK
$ python test_role_based_app.py
..............................
----------------------------------------------------------------------
Ran 30 tests in 42.857s

OK

```
Note: The order of tests should not be changed (i.e first test_app and then test_role_based_app)

<a name="data-modeling"></a>
## Data Modeling
The schema for the database and helper methods are in models.py:
 - There are three tables created: Actors, Movies, Relation.
 - The Actors table has 4 columns: id(primary key), name, age, gender.
 - The Movies table has 3 columns: id(primary key), title, release_date.
 - The Relation table has 2 columns: movie_id(primary key), actor_id(primary key).
 - There is a many-to-many relationship between Actors and Movies table with Relation as an association table.
 - The primary key id of Actors table maps to foreign key actor_id of Relation table.
 - The primary key id of Movies table maps to foreign key movie_id of Relation table.
 - Each table has helper functions for insert, delete, commit and rollback.



<a name="API"></a>
## API Documentation
This documentation will brief you about all the methods that can be used and error behaviour.

### Base URL

**_https://ancient-beyond-36604.herokuapp.com/_**

### Available methods
1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors/id](#delete-actors)
   4. [PATCH /actors/id](#patch-actors)
2. Movies
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies/id](#delete-movies)
   4. [PATCH /movies/id](#patch-movies)
3. Relation
   1. [POST /movies/cast](#post-movies-cast)
   2. [DELETE /movies/cast](#delete-movies-cast)

# <a name="get-actors"></a>
### GET /actors
```bash
$ curl -X GET https://ancient-beyond-36604.herokuapp.com/actors
```
 - Fetches a list of dictionaries in which keys are the ids and values are the rest of the fields.
 - Request Arguments: None
 - Request Headers: An authorization bearer token 
    ```bash
    {"Authorization":token} 
    ```
 - Requires permission: 'get-actors'
 - Return:
   - A list of dictionaries of actors with the following fields:
      1. "id" - id of the actor
      2. "name" - name of the actor.
      3. "age" - age of the actor.
      4. "gender" - gender of the actor.
      5. "movies" - list of all movies the actor has worked or will work
   - A succes field with value being true or false.
 #### Example:
 ```js
 {
  "actors": [
    {
      "age": 27,
      "gender": "male",
      "movies": [
        "matrix"
      ],
      "name": "example"
    }
  ],
  "success": true
}
```
# <a name="post-actors"></a>
### POST /actors
```bash
$ curl -X POST https://ancient-beyond-36604.herokuapp.com/actors 
```
  - Adds a new actor to the database
  - Request Arguments: None
  - Request headers: An authorization bearer token and an application/json header
  ```bash
  {"Authorization":token,"Content-type":"application/json"}
  ```
      1. "name" - required
      2. "age" - required
      3. "gender" - required (only "male", "female" or "not_applicable" accepted)
  - Requires permission: 'post-actors'
  - Returns:\
        "name" - name of creted actor\
        "age" - age of created actor\
        "gender" - gender of created actor\
        "success" - status of request
#### Example
  ```js
  {
  "age": 53,
  "gender": "female",
  "name": "example2",
  "success": true
  }
  ```
#### Error 
If your don't supply any one of the Request header arguments then it will throw a 422 unprocessable error
```js
{
  "error_code": 422,
  "message": "Request unprocessable",
  "success": false
}
```

# <a name="delete-actors"></a>
### DELETE /actors/id
```bash
$ curl -X DELETE https://ancient-beyond-36604.herokuapp.com/actors/1
```
 - Deletes the actor with the specified id.
 - Request Arguments: id of actor
 - Request Header: An authorization bearer token 
    ```bash
    {"Authorization":token} 
    ```
 - Requires permission: 'delete-actors'
 - Returns:\
    "actor_id" - id of deleted actor\
    "success" - request status
#### Example
```js
{
  "actor_id": "1",
  "success": true
}
```
#### Error
Throws a 404 not found error if the given id does not exist.
```js
{
  "error_code": 404,
  "message": "Resource not found",
  "success": false
}
``` 
# <a name="patch-actors"></a>
### PATCH /actors/id
```bash
$ curl -X PATCH https://ancient-beyond-36604.herokuapp.com/actors/1
```
  - Edits the given actor
  - Request Arguments: None
  - Request headers: An authorization bearer token and an application/json header
  ```bash
  {"Authorization":token,"Content-type":"application/json"}
  ```
      1. "name" - not compulsory
      2. "age" - not compulsory
      3. "gender" - not compulsory (only "male", "female" or "not_applicable" accepted)
  - Requires permission: 'patch-actors'
  - Returns:\
        "name" - name of creted actor\
        "age" - age of created actor\
        "gender" - gender of created actor\
        "success" - status of request
#### Example
```js
{
  "age": 53,
  "gender": "male",
  "name": "example2",
  "success": true
}
```
#### Error
If you pass an id which is not available, it throws 404 error.
```js
{
  "error_code": 404,
  "message": "Resource not found",
  "success": false
}
```
If you don't pass allowable value in gender, it will throw 422 error.
```js
{
  "error_code": 422,
  "message": "Request unprocessable",
  "success": false
}
```


# <a name="get-movies"></a>
### GET /movies
```bash
$ curl -X GET https://ancient-beyond-36604.herokuapp.com/movies
```
 - Fetches a list of dictionaries in which keys are the ids and values are the rest of the fields.
 - Request Arguments: None
 - Request Headers: An authorization bearer token 
    ```bash
    {"Authorization":token} 
    ```
 - Requires permission: 'get-movies'
 - Return:
   - A list of dictionaries of movies with the following fields:
      1. "id" - id of the movie
      2. "title" - title of the movie.
      3. "release_date" - release date of the movie.
      5. "actors" - list of all actors in movie
   - A succes field with value being true or false.
 #### Example:
 ```js
 {
  "movies": [
    {
      "actors": [],
      "id": 1,
      "release_date": "Fri, 11 Nov 2011 00:00:00 GMT",
      "title": "matrix"
    }
  ],
  "success": true
}
```

# <a name="post-movies"></a>
### POST /movies
```bash
$ curl -X POST https://ancient-beyond-36604.herokuapp.com/movies 
```
  - Adds a new movie to the database
  - Request Arguments: None
  - Request headers: An authorization bearer token and an application/json header
  ```bash
  {"Authorization":token,"Content-type":"application/json"}
  ```
      1. "title" - required
      2. "release_date" - required (format :: mm/dd/yyyy) 
  - Requires permission: 'post-movies'
  - Returns:\
        "title" - title of created movie\
        "release_date" - release_date of movie\
        "success" - status of request
#### Example
  ```js
 {
  "release_date": "06/15/2012",
  "success": true,
  "title": "Shawshank redumption"
}
  ```
#### Error 
If your don't supply any one of the Request header arguments then it will throw a 422 unprocessable error
```js
{
  "error_code": 422,
  "message": "Request unprocessable",
  "success": false
}
```

# <a name="delete-movies"></a>
### DELETE /movies/id
```bash
$ curl -X DELETE https://ancient-beyond-36604.herokuapp.com/movies/1
```
 - Deletes the movie with the specified id.
 - Request Arguments: id of movie
 - Request Header: An authorization bearer token 
    ```bash
    {"Authorization":token} 
    ```
 - Requires permission: 'delete-movies'
 - Returns:\
    "movie_id" - id of deleted movie\
    "success" - request status
#### Example
```js
{
  "movie_id": "2",
  "success": true
}
```
#### Error
Throws a 404 not found error if the given id does not exist.
```js
{
  "error_code": 404,
  "message": "Resource not found",
  "success": false
}
``` 

# <a name="patch-movies"></a>
### PATCH /movies/id
```bash
$ curl -X PATCH https://ancient-beyond-36604.herokuapp.com/movies/1
```
  - Edits the given movie
  - Request Arguments: None
  - Request headers: An authorization bearer token and an application/json header
  ```bash
  {"Authorization":token,"Content-type":"application/json"}
  ```
      1. "title" - not compulsory
      2. "release_date" - not compulsory (format: mm/dd/yyyy)

  - Requires permission: 'patch-movies'
  - Returns:\
        "title" - title of creted movie\
        "release_date" - release date of created movie\
        "success" - status of request
#### Example
```js
{
  "release_date": "Fri, 11 Nov 2011 00:00:00 GMT",
  "success": true,
  "title": "Godfather"
}
```
#### Error
If you pass an id which does not exist, it throws 404 error.
```js
{
  "error_code": 404,
  "message": "Resource not found",
  "success": false
}
```
If you don't pass appropriate format of release_date, it will throw 422 error.
```js
{
  "error_code": 422,
  "message": "Request unprocessable",
  "success": false
}
```

# <a name="patch-movies-cast"></a>
### POST /movies/cast
```bash
$ curl -X POST https://ancient-beyond-36604.herokuapp.com/movies/cast
```
  - Adds a new actor to specified movie
  - Request Arguments: None
  - Request headers: An authorization bearer token and an application/json header
  ```bash
  {"Authorization":token,"Content-type":"application/json"}
  ```
      1. "movie_id" - required (can be found by GET /movies)
      2. "actor_id" - required (can be found by GET /actors)
  - Requires permission: 'post-movies-cast'
  - Returns:\
        "movie_id" - movie_id assigned to the actor\
        "actor_id" - actor_id assigned to the movie\
        "success" - status of request
#### Example
  ```js
 {
  "actor_id": 2,
  "movie_id": 1,
  "success": true
}
  ```
#### Error 
If your don't supply any one of the Request header arguments then it will throw a 422 unprocessable error
```js
{
  "error_code": 422,
  "message": "Request unprocessable",
  "success": false
}
```
If you supply duplicate values of actor_id and movie_id, it will throw 409 conflict error.  
Also if you add either actor_id or movie_id which dosen't exist, it will throw 409 conflict error.
```js
{
  "error_code": 409,
  "message": "Resource conflict",
  "success": false
}
```

# <a name="delete-movies-cast"></a>
### DELETE /movies/cast/
```bash
$ curl -X DELETE https://ancient-beyond-36604.herokuapp.com/movies/cast/?actor_id=1&movie_id=1
```
 - Deletes actor from the movie with the specified id.
 - Request Arguments: id of actor amd id of movie
 - Request Header: An authorization bearer token 
    ```bash
    {"Authorization":token} 
    ```
 - Requires permission: 'delete-movies-cast'
 - Returns:\
    "movie_id" - id of movie from which actor was deleted\
    "actor_id" - id of deleted actor\
    "success" - request status
#### Example
```js
{
  "actor_id": 2,
  "movie_id": 1,
  "success": true
}
```
#### Error
Throws a 404 not found error if the given actor_id or movie_id does not exist.
```js
{
  "error_code": 404,
  "message": "Resource not found",
  "success": false
}
``` 


<a name="Authentication"></a>
## Authentication
All API endpoints are Auth0 authenticated to use project locally you should configure Auth0 accordingly.

### Auth0 for local use
#### Create an App & API
  1. Create a new account on Auth0. (Ignore this step if already done)
  2. Select Application-> Create Application and choose Regular Web Application.
  3. Goto settings of newly created web application and set callback Url as http://localhost:8080
  4. Select APIs -> Create API and then fill all the information about your API.

#### Create Roles & Permission
  1. Select your created API goto settings and enable RBAC and Add Permissions in the acces token.
  2. Goto Permissions tab and add permissions as given below:
      'get:movies', 'get:actors','post:movies', 'post:actors','post:actor_to_movie','patch:actor',
      'patch:movie','delete:actor','delete:movie','delete:actor_from_movie'
  3. Select user& roles from side menu and then select create roles
  4. Create role casting_assistant and add permissions 'get:actors' and 'get-movies'.
  5. Create role castins_director and add permissions 'get:movies', 'get:actors','post:actors',  
    'post:actor_to_movie','patch:actor', 'patch:movie','delete:actor','delete:actor_from_movie' 
  6. Create role executive_director and add all permissions.

#### Generating Authentication tokens
  1. Select users in side menu and create a new user.
  2. Assign any one role to the user. (i.e casting_assistant, casting_director or executive_director)
  3. Goto api.py and uncomment the generate_auth_url function then goto setup.sh and make changes to the following:
  ```python
  export AUTH0_DOMAIN='dev-d57k6d9t.us.auth0.com'  # your auth0 domain (Goto applications->settings->Domain)
  export API_AUDIENCE='Casting Agency'             # your api audience (Goto API ->settings->identifier)
  export AUTH0_CLIENT_ID='uFWHG4bzzmY4c2Hj6DGLtg9LC715Uf8y' # your client id (Goto applications->settings->Client id)
  export AUTH0_CALLBACK_URL='http://0.0.0.0:8080' # callback url (Goto applications->settings->Allowed Callback URLs)
  ```
  After modifying setup.sh initialize them.
  ```bash
  $ source setup.sh
  ```
  4. From the terminal make a get request to /authorization
  ```bash
  curl http://localhost:8080/authorization
  ```
  5. Goto the returned url you will see a login page and then enter login information of the user which you created before.
  6. You will get a site not reachable error and a jwt token inside the url.
  7. Copy the generated jwt token of the assigned role and paste it in config.py under Authtoken.
  8. Similarly create tokens for all the roles and paste it in setup.sh.
  ```bash
     export CASTING_ASSISTANT='Bearer YOUR_CASTING_ASSISTANT_TOKEN'
     export CASTING_DIRECTOR='Bearer YOUR_CASTING_DIRECTOR_TOKEN'
     export EXECUTIVE_DIRECTOR='Bearer YOUR_EXECUTIVE_DIRECTOR_TOKEN'
  ```
  #### Example tokens
  ```bash
  export CASTING_ASSISTANT='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlcyWXVVcG9OUldVdENyRGFBZUhvYSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kNTdrNmQ5dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxNTM1ODE3ZmY2MGQwMDE5ZDY2YzNjIiwiYXVkIjoiQ2FzdGluZyBBZ2VuY3kiLCJpYXQiOjE1OTUyMjU2NTgsImV4cCI6MTU5NTMxMjA1NSwiYXpwIjoidUZXSEc0Ynp6bVk0YzJIajZER0x0ZzlMQzcxNVVmOHkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.3CiWkPnPyNdI3NnvMP8_7keNWfjK4vjrFL7OWDjCroCHD6H75EIK49quyJh37PnjS9zmU80g6fHmB7dRnLu4sIsPqEXPRvYJJCtNLS5ZTEd6cxJMZWoJVi5nb4onwf5rvWUZ2f6SrisDr_JUWaaWb_TAIww9sCfCzvUZ_6QOhZjsJVORCrM84289powV_dNANRJ0YeSZNvkcuWjjdYRvs24aB67Pzvv-ng5K6c0QvAIGtUbkq_GG_OkcponxkvZetwq3lEKI1zUGxCgzYj133Y_VW46HHnq3J5mN22NIHrdUeztkna7eVyGqt7X-MAgUIkZa9pnamDp3mFyueQI01w'
  export CASTING_DIRECTOR='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlcyWXVVcG9OUldVdENyRGFBZUhvYSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kNTdrNmQ5dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxNTM1ODE3ZmY2MGQwMDE5ZDY2YzNjIiwiYXVkIjoiQ2FzdGluZyBBZ2VuY3kiLCJpYXQiOjE1OTUyMjU3OTUsImV4cCI6MTU5NTMxMjE5MiwiYXpwIjoidUZXSEc0Ynp6bVk0YzJIajZER0x0ZzlMQzcxNVVmOHkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3Rvcl9mcm9tX21vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvcnMiLCJwb3N0OmFjdG9yX3RvX21vdmllIl19.k7-EsWypMQXFElcteFvgghK6kB4iENDRfICI1xjH5IFMnfhfbosDFsBDwbRBxp8fG_WK_v4vUtFSq4UWEpMR_sgdNEN_1eei-qh3RwcDBJKd_FY6AU04VMUDrwuYhSxN6nBEz_EbguUd5VSxuIP7ol2Qm9FmoYPuqQF_fjz0X23nmcTgpXYDkfgRIjiFMQIN6lSbIW3OjF3q3BbnKoPN2owPZNM8RoCIRtsbeHqBD5FdaAzQZvZ3Oq5cThHwvB4vHeH1ZRmdd6fRwZltHDg7meefTwHdsBWo_EZM80CsziQ2Ktm-fyRpXJxF2m6wRuWbaFEF19CpxkR30_midgTat'
  export EXECUTIVE_DIRECTOR='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlcyWXVVcG9OUldVdENyRGFBZUhvYSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kNTdrNmQ5dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxNTM1ODE3ZmY2MGQwMDE5ZDY2YzNjIiwiYXVkIjoiQ2FzdGluZyBBZ2VuY3kiLCJpYXQiOjE1OTUyMjU4NzUsImV4cCI6MTU5NTMxMjI3MiwiYXpwIjoidUZXSEc0Ynp6bVk0YzJIajZER0x0ZzlMQzcxNVVmOHkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3Rvcl9mcm9tX21vdmllIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvcnMiLCJwb3N0OmFjdG9yX3RvX21vdmllIiwicG9zdDptb3ZpZXMiXX0.3jiPSKO2-zhpkDQTH7fcblt9rUdOn7CkQSFcYogIa9KPxWqL17GgONFgc1AuPLryfiSrYGmfdqFPgINqcPafQM5FlhoK5y1b7juhzXlLtUcys5OoBJvMdaUkX4sET3ve54wo36YYU6eF2pCsmPyaATzsSIk0-hycOQBZSVTitGNvA5gXtDEK0g_WTrBXWDdHcL-Z55BxfcPqWS5Qu9a6mP51Y3oPy96v7rBC0EDrdJaZN49vlnGCJBMyMBborhvWODigVLljza7wIGgU6zAD0DcKXj4crmMCMwAsr50awb0541-_XWFpUzI5WwEExV5gFhBfUuN6kAB07VosPad8Og'
  ```

