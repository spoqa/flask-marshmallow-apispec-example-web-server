import functools

from flask import Blueprint, Response, jsonify, request
from werkzeug.exceptions import BadRequest, Unauthorized


blueprint = Blueprint('api', __name__)


def check_access_token(access_token: str) -> bool:
    # TODO: Check Access Token!
    return len(access_token) > 0


def access_token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        access_token = request.headers.get('X-Some-Access-Token')
        if access_token is None:
            raise Unauthorized()
        if not check_access_token(access_token):
            raise Unauthorized()

        return f(*args, **kwargs)

    return decorated


@blueprint.route('/hello/')
def get_hello() -> Response:
    return Response('Hello, world!', 200)


@blueprint.route('/secured/hello/')
@access_token_required
def get_secured_hello() -> Response:
    payload = request.args.to_dict()
    name = payload.get('name', 'unknown')
    return Response(f'Hello, sneaky {name}!', 200)


@blueprint.route('/post/hello/', methods=['POST'])
@access_token_required
def post_hello() -> Response:
    payload = request.get_json()
    try:
        name = payload['name']
        mood = payload['mood']
    except KeyError as e:
        raise BadRequest() from e
    response = {
        'title': f'Hello, {name}!',
        'message': f'I hope your mood {mood!s} be better.',
    }
    return jsonify(response)
