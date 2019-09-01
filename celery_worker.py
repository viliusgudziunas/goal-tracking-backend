import os
from api import celery
from api.factory import create_app
from api.celery_utils import init_celery

app = create_app(os.getenv("FLASK_CONFIG") or "default")
init_celery(celery, app)
