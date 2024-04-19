import os
import sys

from freenit.config import getConfig
from freenit.migration import run_migrations_offline, run_migrations_online

import tilda.app
from alembic import context

sys.path.append(os.getcwd())
config = getConfig()


if context.is_offline_mode():
    run_migrations_offline(config)
else:
    run_migrations_online(config)
