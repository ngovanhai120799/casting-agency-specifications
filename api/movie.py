import json
from datetime import datetime, timedelta
from typing import List

import ulid
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import Response
from werkzeug.exceptions import BadRequest, NotFound, HTTPException

from api.decorator import requires_auth
from models import Movie, db, Actor, Assistant

movie_api = Blueprint("movie", __name__)
DATE_FORMAT = "%Y-%m-%d"

@movie_api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

@movie_api.route("/movies", methods=["GET"])
@cross_origin()
@requires_auth(permission="read:movie")
def get_all_movies():
    list_movies = []
    movies = Movie.query.all()
    for movie in movies:
        response = {
            "id": movie.id,
            "title": movie.title,
            "release_date": movie.release_date,
        }
        list_movies.append(response)
    return jsonify(list_movies)

@movie_api.route("/movies", methods=["POST"])
@cross_origin()
@requires_auth(permission="create:movie")
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
        raise BadRequest("Create movie fail!")

@movie_api.route("/movies/<string:id>", methods=["PATCH"])
@cross_origin()
@requires_auth(permission="update:movie")
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
        raise BadRequest("Update movie fail!")

@movie_api.route("/movies/<string:id>", methods=["DELETE"])
@cross_origin()
@requires_auth(permission="delete:movie")
def delete_movie(id):
    try:
        movie = Movie.query.filter(Movie.id == id).first()
        if not movie:
            raise NotFound(f"Not found movie with id:{id}")
        db.session.delete(movie)
        db.session.commit()
        return jsonify({})
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest("Delete movie fail")

@movie_api.route("/movies/<string:movie_id>/actors/<string:actor_id>", methods=["POST"])
@cross_origin()
@requires_auth(permission="update:movie")
def add_actor_to_movie(movie_id, actor_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if not movie:
            raise NotFound(f"Not found movie with id:{movie_id}")

        list_actors: List[dict] = []
        for assistant in movie.actors:
            if assistant.actor_id == actor_id:
                raise BadRequest("The actor is in the movie!!")
            list_actors.append(assistant.actor.to_dict())

        actor = Actor.query.filter(Actor.id == actor_id).first()
        if not actor:
            raise NotFound(f"Not found actor with id:{actor_id}")

        assistant = Assistant()
        assistant.movie_id = movie_id,
        assistant.actor_id = actor_id

        db.session.add(assistant)
        db.session.commit()
        return jsonify({
            **movie.to_dict(),
            "actors": [*list_actors, actor.to_dict()]
        })
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest("Add actor fail!!")

@movie_api.route("/movies/<string:id>", methods=["GET"])
@cross_origin()
@requires_auth(permission="read:movies")
def get_movie_by_id(id):
    movie = Movie.query.filter(Movie.id == id).first()
    if not movie:
        raise NotFound(f"Not found actor with id: {id}")
    list_actors = []
    for assistant in movie.actors:
        list_actors.append(assistant.actors.to_dict())
    return jsonify({
        **movie.to_dict(),
        "actors": [*list_actors]
    })

@movie_api.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response: Response = e.get_response()
    response.status = e.code
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response