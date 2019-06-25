from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
