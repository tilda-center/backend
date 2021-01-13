from freenit.schemas.base import BaseSchema
from freenit.schemas.role import BaseRoleSchema
from marshmallow import fields


class TokenSchema(BaseSchema):
    email = fields.Email(required=True, description='Email')
    password = fields.Str(required=True, description='Password')


class UserSchema(BaseSchema):
    active = fields.Boolean(description='Activate the user')
    admin = fields.Boolean(description='Is the user admin?')
    email = fields.Email(required=True, description='Email')
    password = fields.Str(
        required=True,
        description='Password',
        load_only=True,
    )
    roles = fields.List(
        fields.Nested(BaseRoleSchema),
        many=True,
        dump_only=True,
    )
    confirmed_at = fields.DateTime(
        description='Time when user was confirmed',
        dump_only=True,
    )


class RefreshSchema(BaseSchema):
    access = fields.Str()
    accessExpire = fields.Integer()
    refreshExpire = fields.Integer()


class LoginSchema(RefreshSchema):
    refresh = fields.Str()


class ResetSchema(BaseSchema):
    token = fields.String(required=True)
    password = fields.String(required=True)
