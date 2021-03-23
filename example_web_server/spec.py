from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint


spec = APISpec(
    title='example-web-server',
    version='0.1.0',
    openapi_version='3.0.2',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
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
