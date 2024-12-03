from datetime import datetime, timedelta

import ulid
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, NotFound, HTTPException

from models import Movie, db
movie_api = Blueprint("movie", __name__)
DATE_FORMAT = "%Y-%m-%d"

@movie_api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

@movie_api.route("/movies", methods=["GET"])
@cross_origin()
def get_all_movies():
    list_movies = []
    movies = Movie.query.all()
    for movie in movies:
        list_movies.append(movie.to_dict())
    return jsonify(list_movies)

@movie_api.route("/movies", methods=["POST"])
@cross_origin()
def create_movie():
    try:
        request_body = request.get_json()
        release_date = datetime.now() + timedelta(days=30)

        movie = Movie()
        movie.id = ulid.ulid()
        movie.title = request_body.get("title")
        movie.release_date = release_date.strftime(DATE_FORMAT)

        db.session.add(movie)
        db.session.commit()
        return jsonify(movie.to_dict())
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest()

@movie_api.route("/movies/<string:id>", methods=["PATCH"])
@cross_origin()
def update_movie(id):
    try:
        movie = Movie.query.filter(Movie.id == id).first()
        if not movie:
            raise NotFound()

        request_body = request.get_json()
        if request_body.get("title"):
            movie.title = request_body.get("title")

        db.session.commit()
        return jsonify(movie.to_dict())
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest()

@movie_api.route("/movies/<string:id>", methods=["DELETE"])
@cross_origin()
def delete_movie(id):
    try:
        movie = Movie.query.filter(Movie.id == id).first()
        if not movie:
            raise NotFound()
        db.session.delete(movie)
        db.session.commit()
        return jsonify({})
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest()

@movie_api.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response