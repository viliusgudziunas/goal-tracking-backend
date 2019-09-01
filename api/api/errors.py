from flask import jsonify
from . import api
from ..exceptions import ValidationError


@api.errorhandler(ValidationError)
def bad_request(e):
    response = jsonify({"error": "bad request", "message": e.args[0]})
    response.status_code = 400
    return response


@api.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({"error": "not found"})
    response.status_code = 404
    return response