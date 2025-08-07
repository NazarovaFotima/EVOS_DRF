import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.py')

app = Celery('EVOS_DRF')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()