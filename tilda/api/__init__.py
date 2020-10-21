from freenit.api import register_endpoints

from .auth import blueprint as auth
from .mail import blueprint as mail
from .blog import blueprint as blog

def create_api(app):
    register_endpoints(
        app,
        '/api/v0',
        [
            auth,
            mail,
            blog,
        ],
    )
