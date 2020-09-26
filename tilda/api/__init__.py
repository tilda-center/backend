from freenit.api import register_endpoints

from .auth import blueprint as auth
from .mail import blueprint as mail


def create_api(app):
    register_endpoints(
        app,
        '/api/v0',
        [
            auth,
            mail,
        ],
    )
