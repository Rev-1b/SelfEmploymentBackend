import os

if os.getenv('DJANGO_ENV') == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *