def create_api(app):
    from freenit.api import register_endpoints

    from .auth import blueprint as auth
    from .mail import blueprint as mail
    from .blog import blueprint as blog

    register_endpoints(
        app,
        '/api/v0',
        [
            auth,
            blog,
            mail,
        ],
    )
