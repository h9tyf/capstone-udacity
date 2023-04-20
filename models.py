import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

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

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

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

  def __init__(self, title, date):
    self.title = title
    self.release_date = date

  def format(self):
    return {
      'id': self.id,
      'title': self.name,
      'release_date': self.release_date}
