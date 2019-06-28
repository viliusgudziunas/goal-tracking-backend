from flask import Blueprint, jsonify, url_for, request, current_app
from . import db
from .models import User, Goal

main = Blueprint("main", __name__)


@main.route("/users/<int:id>")
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@main.route("/users/", methods=["POST"])
def add_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201, {"Location": url_for("main.get_user", id=user.id)}


@main.route("/goals/<int:id>")
def get_goal(id):
    goal = Goal.query.get_or_404(id)
    return jsonify(goal.to_json())


@main.route("/users/<int:id>/goals/")
def get_user_goals(id):
    user = User.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    pagination = user.goals_list.paginate(page, per_page=current_app.config["GOALS_PER_PAGE"], error_out=False)
    goals = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("main.get_user_goals", id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for("main.get_user_goals", id=id, page=page+1)
    return jsonify({
        "goals": [goal.to_json() for goal in goals],
        "prev": prev,
        "next": next
    })
