from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import url_for
from api.exceptions import ValidationError
from . import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    goals_list = db.relationship("Goal", backref="author", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def goals(self):
        return Goal.query.filter_by(author_id=self.id).all()
    
    @staticmethod
    def from_json(json_user):
        email = json_user.get("email")
        password = json_user.get("password")
        return User(email=email, password=password)

    def to_json(self):
        json_user = {
            "goals": [goal.to_json() for goal in self.goals]
        }
        return json_user


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    @staticmethod
    def from_json(json_goal):
        name = json_goal.get("name")
        if name is None or name == "":
            raise ValidationError("Goal does not have a name")
        return Goal(name=name)

    def to_json(self):
        json_goal = {
            "url": url_for("main.get_goal", id=self.id),
            "name": self.name,
            "timestamp": self.timestamp
        }
        return json_goal

