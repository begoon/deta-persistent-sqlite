import logging
import os

import persistent_sqlite
from django.core.wsgi import get_wsgi_application

persistent_sqlite.install()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

LOGGER_FORMAT = ' - '.join(
    ['%(asctime)s', '%(process)d', '%(name)s', '%(levelname)s', '%(message)s']
)

logging.basicConfig(
    format=LOGGER_FORMAT,
    level=logging.INFO,
    force=True,
    handlers=(logging.StreamHandler(),),
)

application = get_wsgi_application()
