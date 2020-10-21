import datetime
import re

from freenit.db import db
from peewee import BooleanField, DateTimeField, ForeignKeyField, TextField
from unidecode import unidecode

from .user import User

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
Model = db.Model


class Blog(Model):
    author = ForeignKeyField(User, backref='blogs')
    content = TextField()
    date = DateTimeField(
        default=datetime.datetime.utcnow
    )
    published = BooleanField()
    slug = TextField()
    title = TextField()
    image = TextField()

    def save(self, *args, **kwargs):
        if self.slug is None:
            result = []
            for word in _punct_re.split(self.title.lower()):
                result.extend(unidecode(word).split())
            self.slug = '-'.join(result)
        super(Blog, self).save(*args, **kwargs)

    @classmethod
    def find(cls, year, month, day, slug):
        intyear = int(year)
        intmonth = int(month)
        intday = int(day)
        startdate_query = Blog.select().where(
            Blog.date >= datetime.date(intyear,
                                       intmonth,
                                       intday)
        )
        enddate_query = startdate_query.where(
            Blog.date < datetime.date(intyear,
                                      intmonth,
                                      intday + 1)
        )
        query = enddate_query.where(Blog.slug == slug)
        if query.count() == 0:
            raise cls.DoesNotExist
        if query.count() > 1:
            raise ValueError('Too many instances')
        return query[0]
