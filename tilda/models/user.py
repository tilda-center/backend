from freenit.models.sql.user import User as BaseUser


class User(BaseUser):
    class Meta:
        table_name = 'users'


class LDAPUser():
    def __init__(self, uid, domain):
        self.uid = uid
        self.domain = domain
