from flask import Flask
from pytest import fixture

from example_web_server import schema, spec
from example_web_server.wsgi import create_wsgi_app


def pytest_configure():
    schema._VALIDATION_ON_DUMP_ENABLED = True
    spec._NO_DOCUMENT_ERROR_ENABLED = True


@fixture
def fx_wsgi_app() -> Flask:
    return create_wsgi_app()
