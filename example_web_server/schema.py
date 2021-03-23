import typing

from marshmallow import Schema, fields

from example_web_server.utils import camelcase


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """
    def on_bind_field(self, field_name: str, field_obj: fields.Field):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


_VALIDATION_ON_DUMP_ENABLED = False


class ValidateOnDumpSchema(Schema):
    """테스트 도중에만 dump를 validate하는 schema.
    """
    def dump(self, obj: typing.Any, *, many: typing.Optional[bool] = None):
        dumped = super().dump(obj, many=many)
        if _VALIDATION_ON_DUMP_ENABLED:
            errors = self.validate(dumped, many=many)
            if errors:
                raise Exception(errors)
        return dumped


class BaseSchema(CamelCaseSchema, ValidateOnDumpSchema):
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
