from flask import Flask, Response, jsonify
from marshmallow import ValidationError

from example_web_server.api import blueprint


def _handle_validation_error(e: ValidationError) -> Response:
    resp = jsonify({'invalidFields': e.normalized_messages()})
    resp.status_code = 400
    return resp


def create_wsgi_app() -> Flask:
    app = Flask(__name__)
    app.register_error_handler(ValidationError, _handle_validation_error)
    app.register_blueprint(blueprint)
    return app
