import os

from celery import Celery

# Maybe problem spot
from django.conf import settings

from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL

app.autodiscover_tasks()


@app.task()
def debug_task():
    sleep(20)
    print('------------------ Celery is working ------------------')
