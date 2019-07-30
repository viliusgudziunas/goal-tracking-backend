import os
from flask_migrate import Migrate
from api import create_app, db
from api.models import User, Goal, GoalInstance

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Goal=Goal, GoalInstance=GoalInstance)
