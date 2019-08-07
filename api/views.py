from flask import Blueprint, jsonify, url_for, request, current_app, g
from . import db
from .models import User, Goal, GoalInstance
from .exceptions import ValidationError

main = Blueprint("main", __name__)

#
# Goal
#
@main.route("/goals/new-goal", methods=["POST"])
def new_goal():
    # Temporary workaround before the login is implemented
    g.current_user = User.query.filter_by(email="coding@example.com").first()
    goal = Goal.from_json(request.json)
    goal.author = g.current_user
    db.session.add(goal)
    db.session.commit()
    return jsonify(goal.to_json()), 201


@main.route("/goals/delete-goal/<int:id>", methods=["POST"])
def delete_goal(id):
    # Temporary workaround before the login is implemented
    g.current_user = User.query.filter_by(email="coding@example.com").first()
    goal = Goal.query.filter_by(id=id).first()
    goal_instances = goal.instances
    for instance in goal_instances:
        db.session.delete(instance)
    db.session.delete(goal)
    db.session.commit()
    return jsonify(g.current_user.goals_to_json()), 200

#
# GoalInstance
#
@main.route("/goals/new-goal-instance", methods=["POST"])
def new_goal_instance():
    goal_id = request.json.get("goal_id")
    goal_instance = GoalInstance.from_json(request.json)
    db.session.add(goal_instance)
    db.session.commit()
    goal = Goal.query.filter_by(id=goal_id).first()
    return jsonify(goal.to_json()), 201


@main.route("/goals/change-goal-target/<int:id>", methods=["POST"])
def change_goal_target(id):
    goal_id = request.json.get("goal_id")
    new_target = request.json.get("target")
    goal = Goal.query.filter_by(id=goal_id).first()
    goal.target = new_target
    db.session.add(goal)
    db.session.commit()
    return jsonify(goal.to_json()), 202

    # @main.route("/users/<int:id>")
    # def get_user(id):
    #     user = User.query.get_or_404(id)
    #     return jsonify(user.goals_to_json())

    # @main.route("/goals/<int:id>")
    # def get_goal(id):
    #     goal = Goal.query.get_or_404(id)
    #     return jsonify(goal.to_json())

    # @main.route("/authenticate", methods=["POST"])
    # def authenticate():
    #     email = request.json.get("email")
    #     password = request.json.get("password")
    #     user = User.query.filter_by(email=email.lower()).first()
    #     if not user:
    #         raise ValidationError("Email or password incorrect")
    #     g.current_user = user
    #     if user.verify_password(password):
    #         print("Hello")
    #         return jsonify({"token": g.current_user.generate_auth_token(expiration=86400), "expiration": 86400})
    #     raise ValidationError("Email or password incorrect")

    # @main.route("/users/", methods=["POST"])
    # def add_user():
    #     user = User.from_json(request.json)
    #     db.session.add(user)
    #     db.session.commit()
    #     return jsonify(user.to_json()), 201, {"Location": url_for("main.get_user", id=user.id)}

    # @main.route("/users/<int:id>/goals/")
    # def get_user_goals(id):
    #     user = User.query.get_or_404(id)
    #     page = request.args.get("page", 1, type=int)
    #     pagination = user.goals_list.paginate(
    #         page, per_page=current_app.config["GOALS_PER_PAGE"], error_out=False)
    #     goals = pagination.items
    #     prev = None
    #     if pagination.has_prev:
    #         prev = url_for("main.get_user_goals", id=id, page=page-1)
    #     next = None
    #     if pagination.has_next:
    #         next = url_for("main.get_user_goals", id=id, page=page+1)
    #     return jsonify({
    #         "goals": [goal.to_json() for goal in goals],
    #         "prev": prev,
    #         "next": next
    #     })
