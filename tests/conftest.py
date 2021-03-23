from flask import Flask
from pytest import fixture

from example_web_server.wsgi import create_wsgi_app


@fixture
def fx_wsgi_app() -> Flask:
    return create_wsgi_app()
