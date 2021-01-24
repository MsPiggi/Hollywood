import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date

db = SQLAlchemy()



DB_HOST = os.getenv('DB_HOST', 'Not set')  
DB_USER = os.getenv('DB_USER', 'Not set')  
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Not set')  
DB_NAME = os.getenv('DB_NAME', 'Not set')  

if DB_HOST == "Not set":
    DB_NAME = "capstone"
    DB_USER = 'postgres'
    DB_PASSWORD = 'Coding2!su'
    DB_HOST = 'localhost:5432'

DB_PATH = os.getenv('DATABASE_URL', 'Not set') 

if DB_PATH == "Not Set": 
    DB_PATH = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD , DB_HOST , DB_NAME)


def setup_db(app, DB_PATH=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    

def db_drop_and_create():
    db.drop_all()
    db.create_all()
    insert_basic_data()

def insert_basic_data():
    actor_basic_data = Actor(name="Keanu Reeves", age=56, gender="Male")
    actor_basic_data.insert()
    actor_basic_data = Actor(name="Carrie-Anne Moss", age=53, gender="Female")
    actor_basic_data.insert()

    movie_basic_data = Movie(title="Matrix 4", release_date=date.today(), imdb_rating=10)
    movie_basic_data.insert()


class Movie(db.Model):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(db.DateTime, nullable=False)
    imdb_rating = Column(Integer, nullable=False)

    def __init__(self, title, release_date, imdb_rating):
        self.title = title
        self.release_date = release_date
        self.imdb_rating = imdb_rating

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
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "imdb_rating": self.imdb_rating
        }


class Actor(db.Model):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

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
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }