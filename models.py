from os import environ as env
from typing import List

from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy import String, Integer, ForeignKey, inspect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

load_dotenv()
db_username = env["DB_USERNAME"]
db_password = env["DB_PASSWORD"]
db_name = env["DB_NAME"]
sqlalchemy_database_uri = f"postgresql+psycopg2://{db_username}:{db_password}@127.0.0.1:5432/{db_name}"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    migrate = Migrate(app, db)
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)

class Assistant(db.Model):
    __tablename__ = "assistants"
    movie_id: Mapped[str] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    actor_id: Mapped[str] = mapped_column(ForeignKey("actors.id"), primary_key=True)
    actor: Mapped["Actor"] = relationship(back_populates="movies")
    movie: Mapped["Movie"] = relationship(back_populates="actors")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Actor(db.Model):
    __tablename__ = 'actors'
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String)
    movies: Mapped[List["Assistant"]] = relationship(back_populates="actor")
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Movie(db.Model):
    __tablename__ = 'movies'
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    release_date: Mapped[str] = mapped_column(String)
    actors: Mapped[List["Assistant"]] = relationship(back_populates="movie")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
