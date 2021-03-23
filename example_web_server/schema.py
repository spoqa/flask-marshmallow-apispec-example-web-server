from marshmallow import Schema, fields

from example_web_server.utils import camelcase


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """
    def on_bind_field(self, field_name: str, field_obj: fields.Field):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class BaseSchema(CamelCaseSchema):
    pass
