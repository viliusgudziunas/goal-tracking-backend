from flask import jsonify
from .views import main
from .exceptions import ValidationError


def bad_request(message):
    response = jsonify({"error": "bad_request", "message": message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({"error": "unauthorized", "message": message})
    response.status_code = 401
    return response


@main.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
