from flask import Flask

from example_web_server.api import blueprint


def create_wsgi_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    return app
