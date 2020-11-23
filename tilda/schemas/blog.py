import sys

from freenit.schemas.base import BaseSchema
from freenit.schemas.paging import PageOutSchema
from marshmallow import fields
from .user import UserSchema


class BlogSchema(BaseSchema):
    id = fields.Integer(description='ID', dump_only=True)
    author = fields.Nested(UserSchema, dump_only=True)
    content = fields.Str(description='Content')
    date = fields.Str(
        description='Time when blog was created',
        # format='YYYY-MM-DDThh:mm:ssTZD',
        dump_only=True,
    )
    published = fields.Boolean(description='Published', default=False)
    slug = fields.String(description='Slug', dump_only=True)
    title = fields.String(description='Title', required=True)
    image = fields.String(description='Image url')

PageOutSchema(BlogSchema, sys.modules[__name__])
