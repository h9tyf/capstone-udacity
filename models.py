import os
from sqlalchemy import Column, String, create_engine
from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  age = Column(db.Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}


class Movie(db.Model):  
  __tablename__ = 'Movie'

  id = Column(db.Integer, primary_key=True)
  title = Column(String)
  release_date = Column(db.DateTime)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}

  @hybrid_property
  def actors(self):
    assigns = Assign.query.filter(Assign.movie_id==self.id).all()
    return [Actor.query.filter(Actor.id==assign.actor_id).first() for assign in assigns]
  

class Assign(db.Model):  
  __tablename__ = 'Assign'

  id = Column(db.Integer, primary_key=True)
  movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'))
  actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'))

  def __init__(self, movie_id, actor_id):
    self.movie_id = movie_id
    self.actor_id = actor_id

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'movie_id': self.movie_id,
      'actor_id': self.actor_id}
