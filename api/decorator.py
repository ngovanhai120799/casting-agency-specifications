import json
from urllib.request import urlopen
from functools import wraps
from os import environ as env

from dotenv import load_dotenv
from flask import request
from jose import jwt
from jose.exceptions import JWTClaimsError, ExpiredSignatureError

from werkzeug.exceptions import Unauthorized, Forbidden, HTTPException

load_dotenv()
# Get Auth0 environment variables
auth0_domain = env["AUTH0_DOMAIN"]
auth0_client_id = env["AUTH0_CLIENT_ID"]
auth0_client_secret = env["AUTH0_CLIENT_SECRET"]
auth0_audience = env["AUTH0_AUDIENCE"]

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = _get_token_auth_header()
                payload = _verify_token_auth(token)
                _check_permission(permission, payload)
                return f(*args, **kwargs)
            except HTTPException as e:
                raise e
        return decorated_function
    return requires_auth_decorator


def _get_token_auth_header():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        raise Unauthorized("Authentication Token is missing!")
    return token


def _verify_token_auth(token):
    jsonurl = urlopen(f'https://{auth0_domain}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise Unauthorized("Authorization malformed.")

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key,
                                 algorithms=["RS256"],
                                 audience=auth0_audience,
                                 issuer='https://' + auth0_domain + '/')
            return payload
        except ExpiredSignatureError:
            raise Unauthorized("Token expired.")
        except JWTClaimsError:
            raise Unauthorized("Incorrect claims. Please, check the audience and issuer.")
        except Exception as e:
            raise Unauthorized("Unable to parse authentication token.")


def _check_permission(permission, payload):
    if "permissions" not in payload:
        raise Forbidden("Unable to parse authentication token.")
    if permission not in payload["permissions"]:
        raise Forbidden("Permission not found.")
    return True