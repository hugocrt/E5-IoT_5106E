# app/__init__.py

from flask import Flask
from .routes import main_blueprint
from elasticsearch import Elasticsearch


def create_app():
    app = Flask(__name__)

    app.elasticsearch = Elasticsearch(["http://elasticsearch:9200"])

    app.register_blueprint(main_blueprint)

    return app
