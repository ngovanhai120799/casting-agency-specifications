import ulid
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, NotFound, HTTPException

from models import Actor, db
actor_api = Blueprint("actor", __name__)

@actor_api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

@actor_api.route("/actors", methods=["GET"])
@cross_origin()
def get_all_actors():
    list_actors = []
    actors = Actor.query.all()
    for actor in actors:
        list_actors.append(actor.to_dict())
    return jsonify(list_actors)

@actor_api.route("/actors", methods=["POST"])
@cross_origin()
def create_actor():
    try:
        request_body = request.get_json()
        actor = Actor()
        actor.id = ulid.ulid()
        actor.name = request_body.get("name")
        actor.age = request_body.get("age")
        actor.gender = request_body.get("gender")

        db.session.add(actor)
        db.session.commit()
        return jsonify(actor.to_dict())
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest()

@actor_api.route("/actors/<string:id>", methods=["PATCH"])
@cross_origin()
def update_actor(id):
    try:
        actor = Actor.query.filter(Actor.id == id).first()
        if not actor:
            raise NotFound()

        request_body = request.get_json()
        if request_body.get("name"):
            actor.name = request_body.get("name")
        if request_body.get("age"):
            actor.age = request_body.get("age")
        if request_body.get("gender"):
            actor.gender = request_body.get("gender")

        db.session.commit()
        return jsonify(actor.to_dict())
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest()

@actor_api.route("/actors/<string:id>", methods=["DELETE"])
@cross_origin()
def delete_actor(id):
    try:
        actor = Actor.query.filter(Actor.id == id).first()
        if not actor:
            raise NotFound()
        db.session.delete(actor)
        db.session.commit()
        return jsonify({})
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest()

# as a decorator
@actor_api.errorhandler(HTTPException)
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