import os

if os.getenv('DJANGO_ENV') == 'production':
    from project.settings_prod import *
else:
    from project.settings_dev import *