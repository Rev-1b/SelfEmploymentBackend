import os

if os.getenv('DJANGO_ENV') == 'production':
    from backend.project.settings_prod import *
else:
    from backend.project.settings_dev import *