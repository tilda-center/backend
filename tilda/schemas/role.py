from freenit.schemas.role import RoleBaseSchema
from marshmallow import fields


class RoleSchema(RoleBaseSchema):
    description = fields.String(description='Description')
    name = fields.String(description='Name')
