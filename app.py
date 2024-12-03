import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

from models import setup_db, db
from api.actor import actor_api
from api.movie import movie_api

load_dotenv()
db_username = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]
sqlalchemy_database_uri = f"postgresql+psycopg2://{db_username}:{db_password}@127.0.0.1:5432/{db_name}"



def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(actor_api)
    app.register_blueprint(movie_api)
    setup_db(app, sqlalchemy_database_uri)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()