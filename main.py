from flask import Flask
from flask_cors import CORS

from api.actor import actor_api
from api.auth import auth
from api.movie import movie_api
from models import setup_db

def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(actor_api)
    app.register_blueprint(movie_api)
    app.register_blueprint(auth)
    setup_db(app)
    return app
