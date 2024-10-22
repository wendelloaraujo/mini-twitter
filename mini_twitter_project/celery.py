import os
from celery import Celery

# Django environment setup for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_twitter_project.settings')

app = Celery('mini_twitter_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()