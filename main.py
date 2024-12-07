from flask import Flask
from flask_cors import CORS

from models import setup_db

app = Flask(__name__)
CORS(app)
def create_app():
    """Application-factory pattern"""
    from api.actor import actor_api
    app.register_blueprint(actor_api)

    from api.movie import movie_api
    app.register_blueprint(movie_api)

    from api.auth import auth
    app.register_blueprint(auth)
    setup_db(app)
    return app
