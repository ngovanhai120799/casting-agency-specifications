from sqlalchemy import Column, String, Integer, inspect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app, sqlalchemy_database_uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    hr = db.relationship('HumanResource', backref='actor', lazy='joined', cascade="all, delete")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(String)
    hr = db.relationship('HumanResource', backref='movie', lazy='joined', cascade="all, delete")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class HumanResource(db.Model):
    __tablename__ = 'human-resources'
    id = Column(String, primary_key=True)
    actor_id = db.Column(db.String(), db.ForeignKey('actors.id'))
    movie_id = db.Column(db.String(), db.ForeignKey('movies.id'))

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}