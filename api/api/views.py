from datetime import datetime, date, timedelta
from flask import jsonify, url_for, request, current_app, g
from .. import db
from ..models import User, Goal, GoalInstance
from . import api


@api.route("/test")
def test():
    today = datetime.combine(date.today(), datetime.min.time())
    instances = [instance.to_json() for instance in GoalInstance.query.all()
                 if instance.timestamp > today]
    return jsonify(instances)


#
# User
#
@api.route("/users/<int:id>")
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.goals_to_json())

#
# Goal
#
@api.route("/goals/new-goal", methods=["POST"])
def new_goal():
    # Temporary workaround before the login is implemented
    g.current_user = User.query.filter_by(email="coding@example.com").first()
    goal = Goal.from_json(request.json)
    goal.author = g.current_user
    db.session.add(goal)
    db.session.commit()
    return jsonify(goal.to_json()), 201


@api.route("/goals/delete-goal/<int:id>", methods=["POST"])
def delete_goal(id):
    # Temporary workaround before the login is implemented
    g.current_user = User.query.filter_by(email="coding@example.com").first()
    goal = Goal.query.filter_by(id=id).first_or_404()
    goal_instances = goal.instances
    for instance in goal_instances:
        db.session.delete(instance)
    db.session.delete(goal)
    db.session.commit()
    return jsonify(g.current_user.goals_to_json()), 200


@api.route("/goals/change-goal/<int:id>", methods=["POST"])
def change_goal(id):
    goal_id = request.json.get("goal_id")
    new_name = request.json.get("name")
    new_target = request.json.get("target")
    goal = Goal.query.filter_by(id=goal_id).first()
    if new_name != "":
        goal.name = new_name
    if new_target != "":
        goal.target = new_target
    db.session.add(goal)
    db.session.commit()
    return jsonify(goal.to_json()), 202

#
# GoalInstance
#
@api.route("/goals/new-goal-instance", methods=["POST"])
def new_goal_instance():
    goal_id = request.json.get("goal_id")
    goal_instance = GoalInstance.from_json(request.json)
    db.session.add(goal_instance)
    db.session.commit()
    goal = Goal.query.filter_by(id=goal_id).first()
    return jsonify(goal.to_json()), 201
