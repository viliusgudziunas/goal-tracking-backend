# from flask import Flask
# from celery import Celery
# from flask_sqlalchemy import SQLAlchemy
# from config import config, Config
# import os

# db = SQLAlchemy()


# def make_celery(app=None):
#     app = app or create_app(os.getenv("FLASK_CONFIG") or "default")
#     celery = Celery(
#         app.import_name,
#         backend=Config.CELERY_RESULT_BACKEND,
#         broker=Config.CELERY_BROKER_URL
#     )
#     celery.conf.update(app.config)

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery


# def create_app(config_name):
#     app = Flask(__name__)
#     app.config.from_object(config[config_name])
#     config[config_name].init_app(app)

#     db.init_app(app)
#     celery = make_celery(app)

#     from .api import api as api_blueprint
#     app.register_blueprint(api_blueprint)

#     return app

##########
#
##########
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy(session_options={"expire_on_commit": False})


def make_celery(app_name=__name__):
    return Celery(
        app_name,
        backend=Config.CELERY_RESULT_BACKEND,
        broker=Config.CELERY_RESULT_BACKEND
    )


celery = make_celery()
