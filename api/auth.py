from os import environ as env

from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, HTTPException

from auth0.authentication import Database, GetToken
auth = Blueprint("auth", __name__)

load_dotenv()
auth0_domain = env["AUTH0_DOMAIN"]
auth0_client_id = env["AUTH0_CLIENT_ID"]
auth0_client_secret = env["AUTH0_CLIENT_SECRET"]
auth0_audience = env["AUTH0_AUDIENCE"]

database = Database(auth0_domain, auth0_client_id)
token = GetToken(domain=auth0_domain, client_id=auth0_client_id, client_secret=auth0_client_secret)


@auth.route("/register", methods=["POST"])
def register():
    try:
        request_body = request.get_json()
        email = request_body.get("email")
        password = request_body.get("password")
        responses = database.signup(email=email, password=password, connection='Username-Password-Authentication')
        return jsonify(responses)
    except HTTPException as e:
        raise BadRequest("Sign-Up user in Auth0 fail!!")


@auth.route("/login", methods=["POST"])
def login():
    try:
        request_body = request.get_json()
        email = request_body.get("email")
        password = request_body.get("password")
        responses = token.login(username=email, password=password, realm='Username-Password-Authentication', audience=auth0_audience)
        return jsonify(responses)
    except HTTPException as e:
        raise BadRequest("Sign-In user in Auth0 fail!!")
