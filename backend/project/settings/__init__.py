import os

from .base import *

if os.getenv('DJANGO_ENV') == 'production':
    from .production import *
elif os.getenv('DJANGO_ENV') == 'development':
    from .development import *
else:
    raise Exception('DJANGO_ENV not defined')