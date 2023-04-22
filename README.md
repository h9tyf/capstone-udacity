# Capstone

[TOC]



## Motivation for the project

This Application is developed for a company that is responsible for creating movies and managing and assigning actors to those movies.

## URL location for the hosted API

The application has been deployed at this [address](https://castpone.onrender.com).

## Run and develop the Application Locally

### Install Dependencies

1. Python3.8.2
2. Virtual Environment
3. Run ` pip install -r requirements.txt` to install dependencies.

### Run

1. Set environment variable

   ```bash
   source setup.sh
   ```

2. Set up the database structure:

   ```bash
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

3. Run

   ```bash
   python app.py
   ```

## Third-Party Authentication

### Role

- Casting Assistant
  - Can view actors and movies

- Casting Director

  - All permissions a Casting Assistant has and…

  - Add or delete an actor from the database

  - Modify actors or movies

- Executive Producer

  - All permissions a Casting Director has and…

  - Add or delete a movie from the database

  - Add or delete an actor from a movie

### User

- assistant
  - email: assistant@assistant.com
  - password: Assistant1
  - Role: Casting Assistant

- deirector
  - email: director@director.com
  - password: Director1
  - Role: Casting Director

- producer
  - email: producer@producer.com
  - password: Producer1
  - Role: Executive Producer

### Third-Party Authentication

#### The Auth0 Domain Name

```
 dev-dlnuifd3dyihlhyz.us.auth0.com
```

#### auth steps

1. Use url below to get tokens for different users.

   ```
   https://dev-dlnuifd3dyihlhyz.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=1cTw2peHIv0GvfkYwNt8bXHTnQ1McYQ6&redirect_uri=http://127.0.0.1:3000/callback
   ```

2. Users's email and password have been listed in part "User".

3. Put tokens in file ` setup.sh` so that you can use tokens to perform different operations.  I have put the token valid for one day in the `setup.sh` file.

## Test

There are two files used for test, one for local testing and one for remote testing. Three of all tests are for auth tests, if there is no problem, it will eventually prompt **three test failures**.

**Before run ` setup.sh`，make sure that tokens in this file is valid.**

### run test file locally

1. Set environment variable

   ```bash
   source setup.sh
   ```

2. run test file

   ```bash
   python test_local.py
   ```

### run test for remote api

1. Set environment variable

   ```bash
   source setup.sh
   ```

2. run test file

   ```
   python test.py
   ```

## Model

### Actor

| column |         |
| ------ | ------- |
| name   | String  |
| age    | Integer |
| gender | String  |

### Movie

| column       |          |
| ------------ | -------- |
| title        | String   |
| release_date | datetime |

### Assign

| column   |         |
| -------- | ------- |
| movie_id | Integer |
| actor_id | Integer |

## API

` GET '/actors'`

- get all actors

- Request: None

- Response: information of all actors

  ```python
  {
      'actors': [
          {'age': 26, 'gender': 'female', 'id': 1, 'name': 'Jane'}, 
          {'age': 25, 'gender': 'male', 'id': 2, 'name': 'Tom'}, 
          {'age': 27, 'gender': 'male', 'id': 3, 'name': 'Ken'}
      ], 
      'success': True, 
      'total_actors': 3}
  ```

` POST '/actors'`

- create an new actor

- Request: information of an actor

  ```python
  {
      'name': 'Jane',
      'age': 22, 
      'gender':'female'
  }
  ```

- Response: 

  ```python
  {
      'created': 1, 
      'success': True
  }
  ```

` PATCH '/actors/${actor_id}'`

- modify information of an actor

- Request: id and information of an actor

  ```python
  {
      'name': 'Jane',
      'age': 26, 
      'gender':'female'
  }
  ```

- Response: actor' id

  ```python
  {
      'edited': 1, 
      'success': True
  }
  ```

` DELETE '/actors/${actor_id}'`

- delete an actor from database

- Request:  id of an actor

- Response: actor' id

  ```python
  {
      'deleted': 3, 
      'success': True
  }
  ```

` GET '/movies'`

- get all movies

- Request: None

- Response:

  ```python
  {
      'movies': [
          {'id': 1, 'release_date': 'Wed, 30 Jun 2021 20:15:00 GMT', 'title': 'Gone with the Wind'}, 
          {'id': 2, 'release_date': 'Tue, 14 Dec 2010 16:00:00 GMT', 'title': 'Coco'}], 
      'success': True, 
      'total_movies': 2}
  ```

` POST '/movies'`

- create a new movie

- Request:  information of a movie

  ```python
  {
      'title': 'Gone with the Wind',
      'release_date': 1625112900# unix_timestamp
  }
  ```

- Response: 

  ```python
  {
      'created': 1, 
      'success': True
  }
  ```

` PATCH '/movies/${movie_id}'`

- modify information of a movie

- Request: id and information of a movie

  ```python
  {
      'title': 'Gone with the Wind',
      'release_date': 1638332100# unix_timestamp
  }
  ```

- Response: movie's id

  ```python
  {
      'edited': 1, 
      'success': True
  }
  ```

` DELETE '/movies/${movie_id}'`

- delete a movie from database

- Request:  id of a movie

- Response: movie's id

  ```python
  {
      'deleted': 2, 
      'success': True
  }
  ```

` GET '/movies/${movie_id>}/actors'`

- get all actors of a movie

- Request: id of a movie

- Response:

  ```python
  {
      'actors': [
          {'age': 22, 'gender': 'female', 'id': 1, 'name': 'Jane'}, 
          {'age': 25, 'gender': 'male', 'id': 2, 'name': 'Tom'}], 
      'success': True, 
      'total_actors': 2
  }
  ```

`POST '/movies/${movie_id>}/actors/${actor_id}'`

- assign an actor to a movie

- Request: movie's id and actor's id

- Response:

  ```python
  {
      'created': 4, # assign' id
      'success': True
  }
  ```

`DELETE '/movies/${movie_id>}/actors/${actor_id}'`

- detele an actor from a movie

- Request:movie's id and actor's id

- Response:

  ```python
  {
      'deleted': 2,  # assign' id
      'success': True
  }
  ```

  

