import os
from flask import Flask
from config import config

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


def create_app(config_name, app_name=PKG_NAME, **kwargs):
    app = Flask(app_name)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from . import db
    db.init_app(app)

    if kwargs.get("celery"):
        from .celery_utils import init_celery
        init_celery(kwargs.get("celery"), app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
