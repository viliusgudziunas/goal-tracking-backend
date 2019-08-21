from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
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

    # def generate_auth_token(self, expiration):
    #     s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    #     return s.dumps({"id": self.id}).decode("utf-8")

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(current_app.config["SECRET_KEY"])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return None
    #     return User.query.get(data["id"])

    # @staticmethod
    # def from_json(json_user):
    #     email = json_user.get("email")
    #     password = json_user.get("password")
    #     return User(email=email, password=password)

    def to_json(self):
        json_user = {
            "goals": self.goals_to_json
        }
        return json_user

    @property
    def goals(self):
        return Goal.query.filter_by(author_id=self.id).all()

    def goals_to_json(self):
        return [goal.to_json() for goal in self.goals]

    # def get_goal(self, name):
    #     return Goal.query.filter_by(author_id=self.id, name=name).first()


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    target_type = db.Column(db.Integer)
    target = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    instances_list = db.relationship(
        "GoalInstance", backref="goal", lazy="dynamic")

    @staticmethod
    def from_json(json_goal):
        name = json_goal.get("name")
        target_type = int(json_goal.get("target_type"))
        target = int(json_goal.get("target"))
        if name is None or name == "":
            raise ValidationError("Goal does not have a name")
        if target_type is None or target_type == "":
            raise ValidationError("Goal does not have a target type")
        if target is None or target == "":
            raise ValidationError("Goal does not have a target")
        return Goal(name=name, target_type=target_type, target=target)

    def to_json(self):
        json_goal = {
            "id": self.id,
            "name": self.name,
            "target_type": self.target_type,
            "target": self.target,
            "timestamp": self.date,
            "instances": [instance.to_json() for instance in self.instances]
        }
        return json_goal

    @property
    def instances(self):
        return GoalInstance.query.filter_by(goal_id=self.id).all()

    @property
    def date(self):
        return self.timestamp.strftime("%a %b %d %Y %H:%M:%S")


class GoalInstance(db.Model):
    __tablename__ = "goal instances"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    hours_completed = db.Column(db.Float)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))

    @staticmethod
    def from_json(json_goal_instance):
        goal_id = json_goal_instance.get("goal_id")
        if goal_id is None or goal_id == "":
            raise ValidationError("Goal instance does not have a goal ID")
        hours_completed = json_goal_instance.get("hours_completed")
        if hours_completed is None or hours_completed == "":
            return GoalInstance(goal_id=goal_id)
        return GoalInstance(goal_id=goal_id, hours_completed=hours_completed)

    def to_json(self):
        json_goal_instance = {
            "id": self.id,
            "goal_id": self.goal_id,
            "timestamp": self.date,
        }
        goal = Goal.query.filter_by(id=self.goal_id).first()
        if goal.target_type == 2:
            json_goal_instance["hours_completed"] = self.hours_completed
        return json_goal_instance

    @property
    def date(self):
        return self.timestamp.strftime("%a %b %d %Y %H:%M:%S")
