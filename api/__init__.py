from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_httpauth import HTTPBasicAuth
from config import config

db = SQLAlchemy()
# auth = HTTPBasicAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
