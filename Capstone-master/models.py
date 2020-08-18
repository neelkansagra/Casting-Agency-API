import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from config import database
import json

# Uncomment this while connecting to heroku
database_path = os.environ['DATABASE_URL']

# Uncomment this while connecting locally
""" database_path = "postgresql://{}:{}@{}/{}".format(
            database["username"], database["username_password"],
            database["port"], database["database_name"])
 """
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Relation(db.Model):
    __tablename__ = 'relation'
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.id'), primary_key=True)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def commit():
        db.session.commit()
        db.session.close()

    def rollback():
        db.session.rollback()
        db.session.close()


class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    release_date = Column(db.Date)
    actors = relationship("Actors", secondary='relation',
                          back_populates="movies")

    def __init__(self, title, release_date=release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def rollback():
        db.session.rollback()
        db.session.close()

    def commit():
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def format(self, actors):
        d = {"id": self.id, "title": self.title,
             "release_date": self.release_date, "actors": actors}
        return d


class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    age = Column(db.Integer)
    movies = relationship("Movies", secondary='relation',
                          back_populates="actors")
    gender = Column(ENUM("female", "male", "not_applicable", name="gender"))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def rollback():
        db.session.rollback()
        db.session.close()

    def commit():
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def format(self, movies):
        d = {"id": self.id, "name": self.name, "age": self.age,
             "gender": self.gender, "movies": movies}
        return d
