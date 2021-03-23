import typing

from apispec import APISpec, BasePlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint

from example_web_server.utils import camelcase


class AccessTokenPlugin(BasePlugin):
    """액세스 토큰을 사용하는 API 엔드포인트들에게 관련 문서를 자동으로 추가합니다.
    """

    def init_spec(self, spec: APISpec):
        spec.components.security_scheme(
            'access_token',
            {
                'type': 'apiKey',
                'description': '액세스 토큰',
                'name': 'X-Some-Access-Token',
                'in': 'header',
            },
        )

    def path_helper(self, operations: dict, *, view, **kwargs):
        if getattr(view, '__access_token_required', False):
            for operation in operations.values():
                operation.setdefault('security', []).append({
                    'access_token': [],
                })
                operation.setdefault('responses', {}).update({
                    401: {'description': '액세스 토큰이 잘못됨'},
                })


def document_validation_error(f):
    f.__validation_error_documentation_needed = True
    return f


class ValidationErrorPlugin(BasePlugin):
    """marshmallow ValidationError가 발생할 수 있는 API(document_validation_error
    데코레이터로 마킹합니다)에 관련 문서와 스키마를 붙여줍니다.
    """

    def path_helper(self, operations: dict, *, view, **kwargs):
        for operation in operations.values():
            responses = response = operation.setdefault('responses', {})
            if getattr(view, '__validation_error_documentation_needed', False):
                response = responses.setdefault(400, {})
                response.setdefault(
                    'description',
                    '요청 검증에 실패함. `invalidFields` 항목에서 검증에 실패한 '
                    '필드와 에러 메시지를 확인할 수 있습니다.',
                )
                response \
                    .setdefault('content', {}) \
                    .setdefault('application/json', {}) \
                    .setdefault('schema', 'ValidationErrorSchema')


class BasicInfoPlugin(BasePlugin):
    """operationId와 summary를 path와 엔드포인트 함수 이름에서 자동으로 생성합니다.
    """

    def path_helper(
        self,
        operations: dict,
        *,
        view: typing.Callable,
        path: str,
        blueprint_name: str,
        **kwargs,
    ):
        for operation in operations.values():
            operation_id = camelcase(view.__name__)
            summary = path + ' ' + operation_id
            operation.setdefault('operationId', operation_id)
            operation.setdefault('summary', summary)
            operation.setdefault('tags', []).append(blueprint_name)


spec = APISpec(
    title='example-web-server',
    version='0.1.0',
    openapi_version='3.0.2',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
        AccessTokenPlugin(),
        ValidationErrorPlugin(),
        BasicInfoPlugin(),
    ],
)


# https://github.com/marshmallow-code/apispec-webframeworks/pull/27
class DocumentedBlueprint(Blueprint):
    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)
        self.view_functions = []

    def add_url_rule(
        self,
        rule,
        endpoint=None,
        view_func=None,
        **kwargs,
    ):
        super().add_url_rule(
            rule,
            endpoint=endpoint,
            view_func=view_func,
            **kwargs,
        )
        self.view_functions.append(view_func)

    def register(self, app, options, first_registration=False):
        super().register(app, options, first_registration=first_registration)
        for view_function in self.view_functions:
            spec.path(view=view_function, app=app, blueprint_name=self.name)
