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


class ValidationErrorSchema(BaseSchema):
    invalid_fields = fields.Mapping(
        keys=fields.String,
        values=fields.List(fields.String),
        metadata={
            'description': '검증에 실패한 필드 이름과 에러 목록',
            'example': {'someField': ['some error']},
        },
    )
