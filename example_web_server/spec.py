from apispec import APISpec, BasePlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint


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


spec = APISpec(
    title='example-web-server',
    version='0.1.0',
    openapi_version='3.0.2',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
        AccessTokenPlugin(),
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
            spec.path(view=view_function, app=app)
