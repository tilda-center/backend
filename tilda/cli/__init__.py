from cryptography.fernet import Fernet
from flask.cli import AppGroup

key_group = AppGroup('key', short_help='Manage keys')


def register_key(app):
    @key_group.command()
    def generate():
        key = Fernet.generate_key()
        root = app.config['PROJECT_ROOT']
        key_path = f'{root}/secret.key'
        with open(key_path, 'wb') as key_file:
            key_file.write(key)

    app.cli.add_command(key_group)


def register(app):
    register_key(app)
