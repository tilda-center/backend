import os
import socket
from importlib import import_module

from freenit import create_app

from config import configs
from name import app_name
from tilda.cli import register

api = import_module(f'{app_name}.api')
config_name = os.getenv('FLASK_ENV') or 'default'
config = configs[config_name]
schemas = {
    'user': f'{app_name}.schemas.user',
    'role': f'{app_name}.schemas.role',
}
application = create_app(config, dbtype='sql', schemas=schemas)
api.create_api(application)
register(application)
hostname = socket.gethostname()
port = os.environ.get('FLASK_PORT', 5000)
SWAGGER_PATH = f'{config.OPENAPI_URL_PREFIX}{config.OPENAPI_SWAGGER_UI_PATH}'
SWAGGER_URL = f'http://{hostname}:{port}{SWAGGER_PATH}'

if __name__ == '__main__':
    print(' * Swagger URL:', SWAGGER_URL)
    application.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        use_reloader=True,
    )
