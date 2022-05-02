import os
from celery import Celery
import celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

celery = Celery("core")
celery.config_from_object("django.conf:settings",namespace='CELERY')
celery.autodiscover_tasks()