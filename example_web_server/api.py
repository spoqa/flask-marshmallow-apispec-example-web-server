import functools

from flask import Blueprint, Response, jsonify, request
from marshmallow import fields
from werkzeug.exceptions import Unauthorized

from example_web_server.schema import BaseSchema

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


class GetSecuredHelloArgsSchema(BaseSchema):
    name = fields.String(
        missing='unknown',
        metadata={
            'description': '당신의 이름. (기본값: unknown)',
            'example': 'Thomas',
        },
    )


get_secured_hello_args_schema = GetSecuredHelloArgsSchema()


@blueprint.route('/secured/hello/')
@access_token_required
def get_secured_hello() -> Response:
    payload = get_secured_hello_args_schema.load(request.args.to_dict())
    name = payload['name']
    return Response(f'Hello, sneaky {name}!', 200)


class PostHelloRequestSchema(BaseSchema):
    name = fields.String(
        required=True,
        metadata={
            'description': '당신의 이름',
            'example': 'Thomas',
        },
    )
    mood = fields.Integer(
        required=True,
        metadata={
            'description': '당신의 현재 기분',
            'example': 5,
        },
    )


class PostHelloResponseSchema(BaseSchema):
    title = fields.String(required=True)
    message = fields.String(required=True)


post_hello_request_schema = PostHelloRequestSchema()
post_hello_response_schema = PostHelloResponseSchema()


@blueprint.route('/post/hello/', methods=['POST'])
@access_token_required
def post_hello() -> Response:
    payload = post_hello_request_schema.load(request.get_json())
    name = payload['name']
    mood = payload['mood']
    response = {
        'title': f'Hello, {name}!',
        'message': f'I hope your mood {mood!s} be better.',
    }
    return jsonify(post_hello_response_schema.dump(response))
