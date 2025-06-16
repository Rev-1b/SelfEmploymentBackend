import os
import django

from time import sleep
# probably testing legacy, should be -------------------- 'project.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.conf import settings
from celery import Celery

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL

app.autodiscover_tasks()


@app.task()
def debug_task():
    sleep(20)
    print('------------------ Celery is working ------------------')
