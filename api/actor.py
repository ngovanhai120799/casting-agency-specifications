import json

import ulid
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import Response
from werkzeug.exceptions import BadRequest, NotFound, HTTPException

from models import Actor, db
from api.decorator import requires_auth

actor_api = Blueprint("actor", __name__)

@actor_api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

@actor_api.route("/actors", methods=["GET"])
@cross_origin()
@requires_auth(permission="read:actor")
def get_all_actors():
    list_actors = []
    actors = Actor.query.all()
    for actor in actors:
        list_actors.append(actor.to_dict())
    return jsonify(list_actors)

@actor_api.route("/actors", methods=["POST"])
@cross_origin()
@requires_auth(permission="create:actor")
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
        raise BadRequest("Create new actor fail!!!")

@actor_api.route("/actors/<string:id>", methods=["PATCH"])
@cross_origin()
@requires_auth(permission="update:actor")
def update_actor(id):
    try:
        actor = Actor.query.filter(Actor.id == id).first()
        if not actor:
            raise NotFound(f"Not found actor with id: {id}")

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
        raise BadRequest("Update actor fail!!!")

@actor_api.route("/actors/<string:id>", methods=["DELETE"])
@cross_origin()
@requires_auth(permission="delete:actor")
def delete_actor(id):
    try:
        actor = Actor.query.filter(Actor.id == id).first()
        if not actor:
            raise NotFound(f"Not found actor with id: {id}")
        db.session.delete(actor)
        db.session.commit()
        return jsonify({})
    except SQLAlchemyError as err:
        db.session.rollback()
        raise BadRequest("Delete actor fail")


@actor_api.errorhandler(HTTPException)
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